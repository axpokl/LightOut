param(
  [string]$TimeFile = (Join-Path $PSScriptRoot 'time.txt'),
  [string]$MusicDir = (Join-Path $PSScriptRoot '3_music_fin'),
  [string]$OutFile  = (Join-Path $PSScriptRoot 'bgm.mp3'),
  [string]$Ffmpeg   = 'ffmpeg',
  [string]$Ffprobe  = 'ffprobe',
  [switch]$ForceMix,
  [switch]$KeepTemp
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-SecondsFromTime([string]$s){
  $s = $s.Trim()
  $fmt = 'hh\:mm\:ss\.fff'
  try { return [TimeSpan]::ParseExact($s, $fmt, [Globalization.CultureInfo]::InvariantCulture).TotalSeconds } catch {}
  return ([TimeSpan]::Parse($s, [Globalization.CultureInfo]::InvariantCulture)).TotalSeconds
}

function Parse-Line([string]$line){
  if([string]::IsNullOrWhiteSpace($line)){ return $null }
  $p = $line -split "`t"
  if($p.Count -lt 2){ $p = $line -split '\s+' }
  if($p.Count -lt 2){ throw "Bad line: $line" }

  $a = $p[0].Trim()
  $b = $p[1].Trim()
  $timeRe = '^\d{2}:\d{2}:\d{2}(\.\d{1,3})?$'

  if($a -match $timeRe){ return [pscustomobject]@{ Start=$a; Name=$b } }
  if($b -match $timeRe){ return [pscustomobject]@{ Start=$b; Name=$a } }
  throw "Cannot find time in line: $line"
}

function ProbeDuration([string]$path){
  $out = & $Ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -- "$path"
  if($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($out)){ throw "ffprobe duration failed: $path" }
  return [double]::Parse($out.Trim(), [Globalization.CultureInfo]::InvariantCulture)
}

function ProbeAudio([string]$path){
  $json = & $Ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate,channels,channel_layout,bit_rate -of json -- "$path"
  if($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($json)){ throw "ffprobe audio failed: $path" }
  $o = $json | ConvertFrom-Json
  $s = $o.streams[0]
  $sr = [int]$s.sample_rate
  $ch = [int]$s.channels
  $cl = if($s.channel_layout){ [string]$s.channel_layout } elseif($ch -eq 1){ 'mono' } else { 'stereo' }
  $br = if($s.bit_rate){ [int]$s.bit_rate } else { $null }
  [pscustomobject]@{ SampleRate=$sr; Channels=$ch; ChannelLayout=$cl; BitRate=$br }
}

$lines = Get-Content -LiteralPath $TimeFile -Encoding UTF8 | Where-Object { $_ -and $_.Trim() -ne '' }
$raw = foreach($l in $lines){ Parse-Line $l }
$raw = $raw | Where-Object { $_ -ne $null }

if($raw.Count -eq 0){ throw "No entries in $TimeFile" }
if(!(Test-Path -LiteralPath $MusicDir)){ throw "Missing folder: $MusicDir" }

$items = $raw | ForEach-Object {
  $name = $_.Name
  $path = Join-Path $MusicDir $name
  if(!(Test-Path -LiteralPath $path)){ throw "Missing file: $path" }
  [pscustomobject]@{
    Name = $name
    Path = $path
    StartSeconds = (Get-SecondsFromTime $_.Start)
  }
} | Sort-Object StartSeconds

$audio = ProbeAudio $items[0].Path

$tmpDir = Join-Path $PSScriptRoot "_tmp_bgm"
New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null
$concatFile = Join-Path $tmpDir "concat.txt"

function MakeSilence([double]$dur, [int]$idx){
  $dur = [Math]::Round($dur, 3)
  if($dur -le 0){ return $null }
  $out = Join-Path $tmpDir ("silence_{0:d4}.mp3" -f $idx)
  $lavfi = "anullsrc=r=$($audio.SampleRate):cl=$($audio.ChannelLayout)"
  $args = @('-hide_banner','-loglevel','error','-f','lavfi','-i',$lavfi,'-t',"$dur")
  if($audio.BitRate){ $args += @('-c:a','libmp3lame','-b:a',"$($audio.BitRate)") } else { $args += @('-c:a','libmp3lame','-q:a','2') }
  $args += @('-ar',"$($audio.SampleRate)",'-ac',"$($audio.Channels)",'-y',$out)
  & $Ffmpeg @args
  if($LASTEXITCODE -ne 0){ throw "Failed to create silence: $dur sec" }
  return $out
}

function TryConcatCopy(){
  $segIdx = 1
  $segments = New-Object System.Collections.Generic.List[string]

  $lead = $items[0].StartSeconds
  if($lead -gt 0.0005){
    $s = MakeSilence $lead ($segIdx++)
    if($s){ $segments.Add($s) }
  }

  for($i=0; $i -lt $items.Count; $i++){
    $segments.Add($items[$i].Path)
    if($i -eq $items.Count - 1){ break }

    $dur = ProbeDuration $items[$i].Path
    $pad = $items[$i+1].StartSeconds - ($items[$i].StartSeconds + $dur)

    if($pad -lt -0.02){ return $false }

    if($pad -gt 0.0005){
      $s = MakeSilence $pad ($segIdx++)
      if($s){ $segments.Add($s) }
    }
  }

  $content = $segments | ForEach-Object {
    $p = $_ -replace "'", "''"
    "file '$p'"
  }

  $enc = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllLines($concatFile, $content, $enc)

  & $Ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i $concatFile -c copy -y $OutFile
  return ($LASTEXITCODE -eq 0)
}

function MixEncode(){
  $args = New-Object System.Collections.Generic.List[string]
  $args.AddRange([string[]]@('-hide_banner','-loglevel','error'))
  foreach($it in $items){ $args.AddRange([string[]]@('-i',"$($it.Path)")) }

  $filters = New-Object System.Collections.Generic.List[string]
  for($i=0; $i -lt $items.Count; $i++){
    $d = [int][Math]::Round($items[$i].StartSeconds * 1000.0)
    $filters.Add("[$i:a]adelay=$d|$d[a$i]")
  }
  $mixInputs = (0..($items.Count-1) | ForEach-Object { "[a$_]" }) -join ''
  $filters.Add("$mixInputs`amix=inputs=$($items.Count):duration=longest:dropout_transition=0[outa]")
  $fc = ($filters -join ';')

  $args.AddRange([string[]]@('-filter_complex',$fc,'-map','[outa]'))
  if($audio.BitRate){ $args.AddRange([string[]]@('-c:a','libmp3lame','-b:a',"$($audio.BitRate)")) } else { $args.AddRange([string[]]@('-c:a','libmp3lame','-q:a','2')) }
  $args.AddRange([string[]]@('-ar',"$($audio.SampleRate)",'-ac',"$($audio.Channels)",'-y',"$OutFile"))

  & $Ffmpeg $args.ToArray()
  if($LASTEXITCODE -ne 0){ throw "ffmpeg mix failed" }
}

$ok = $false
try{
  if(-not $ForceMix){
    try{ $ok = TryConcatCopy } catch { $ok = $false }
  }
  if(-not $ok){ MixEncode }
}
finally{
  if(-not $KeepTemp){
    Remove-Item -LiteralPath $tmpDir -Recurse -Force -ErrorAction SilentlyContinue
  }
}
