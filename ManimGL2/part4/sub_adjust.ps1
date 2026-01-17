param(
  [ValidateSet('silence','sine')]
  [string]$InsertMarker = 'sine',
  [double]$MarkerFreqHz = 880,
  [double]$MarkerVolume = 0.25
)

$ErrorActionPreference = 'Stop'

$inv = [System.Globalization.CultureInfo]::InvariantCulture
function F([double]$x) { [string]::Format($inv, '{0:0.000}', $x) }

function WriteUtf8NoBom([string]$path, [string]$text) {
  $enc = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($path, $text, $enc)
}

function ParseTimeToSeconds([string]$s) {
  $s = $s.Trim()
  $m = [regex]::Match($s, '^(?<h>\d{2,}):(?<m>\d{2}):(?<s>\d{2})(?:\.(?<ms>\d{1,3}))?$')
  if (-not $m.Success) { throw "Bad time format: $s (need HH:MM:SS.mmm)" }
  $h = [int]$m.Groups['h'].Value
  $min = [int]$m.Groups['m'].Value
  $sec = [int]$m.Groups['s'].Value
  $ms = 0
  if ($m.Groups['ms'].Success) {
    $msStr = $m.Groups['ms'].Value.PadRight(3, '0')
    $ms = [int]$msStr
  }
  return ($h * 3600.0) + ($min * 60.0) + $sec + ($ms / 1000.0)
}

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw 'ffmpeg not found in PATH' }
if (-not (Get-Command ffprobe -ErrorAction SilentlyContinue)) { throw 'ffprobe not found in PATH' }

$workDir = (Get-Location).Path
$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { $workDir }

$toolDir = $scriptDir
$subInScript = Join-Path $scriptDir 'subtitle.ps1'
$subInWork = Join-Path $workDir 'subtitle.ps1'
if (-not (Test-Path -LiteralPath $subInScript) -and (Test-Path -LiteralPath $subInWork)) { $toolDir = $workDir }

$adjFile = Join-Path $workDir 'sub_adjust.txt'
if (-not (Test-Path -LiteralPath $adjFile)) {
  $adjFile = Join-Path $scriptDir 'sub_adjust.txt'
}
if (-not (Test-Path -LiteralPath $adjFile)) { throw "sub_adjust.txt not found in current folder or script folder: $workDir / $scriptDir" }

$mp3 = Get-ChildItem -LiteralPath $workDir -File -Filter *.mp3 |
  Where-Object { $_.BaseName -match '^\d+$' } |
  Sort-Object { [Int64]$_.BaseName } -Descending |
  Select-Object -First 1
if (-not $mp3) { throw 'No numeric mp3 found in current directory (e.g. 1768642112769.mp3)' }
$inMp3 = $mp3.FullName

$videosDir = Join-Path $workDir 'videos'
New-Item -ItemType Directory -Path $videosDir -Force | Out-Null

$inVideo = Join-Path $videosDir 'lights_out.mp4'
if (-not (Test-Path -LiteralPath $inVideo)) { throw "Missing video: $inVideo" }

$outMp3 = Join-Path $videosDir 'subtitle.mp3'
$outVideo = Join-Path $videosDir 'lights_out_audio.mp4'

$helperDir = Join-Path $toolDir 'adjust_scripts'
New-Item -ItemType Directory -Path $helperDir -Force | Out-Null
$filterScript = Join-Path $helperDir 'filter_complex.txt'
$helperPath = Join-Path $helperDir 'run_adjust_generated.ps1'

$items = @()
Get-Content -LiteralPath $adjFile | ForEach-Object {
  $l = $_.Trim()
  if (-not $l) { return }
  if ($l -match '^\s*#') { return }
  $p = $l -split '\s+'
  if ($p.Count -lt 2) { throw "Bad line (need: <time><tab><delta>): $l" }
  $t = ParseTimeToSeconds $p[0]
  $d = [double]::Parse($p[1], $inv)
  $items += [pscustomobject]@{ Time = $t; Delta = $d; Raw = $l }
}
$items = $items | Sort-Object Time
if ($items.Count -lt 1) { throw 'sub_adjust.txt has no data' }
for ($i = 1; $i -lt $items.Count; $i++) {
  if ($items[$i].Time -le $items[$i - 1].Time) {
    throw "Times must be strictly increasing:`n$($items[$i-1].Raw)`n$($items[$i].Raw)"
  }
}

$durText = (& ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $inMp3) | Select-Object -First 1
$durText = ($durText | Out-String).Trim()
$dur = [double]::Parse($durText, $inv)
if ($dur -le 0) { throw 'Failed to get duration from ffprobe' }

$sr = 16000
$cl = 'mono'

$N = $items.Count
$segStart = New-Object double[] ($N + 1)
$segEnd = New-Object double[] ($N + 1)

$segStart[0] = 0
$segEnd[0] = $items[0].Time - [Math]::Max($items[0].Delta, 0)

for ($k = 1; $k -lt $N; $k++) {
  $segStart[$k] = $items[$k - 1].Time
  $segEnd[$k] = $items[$k].Time - [Math]::Max($items[$k].Delta, 0)
}

$segStart[$N] = $items[$N - 1].Time
$segEnd[$N] = $dur

for ($k = 0; $k -le $N; $k++) {
  if ($segStart[$k] -lt 0) { $segStart[$k] = 0 }
  if ($segEnd[$k] -lt 0) { $segEnd[$k] = 0 }
  if ($segEnd[$k] -gt $dur) { $segEnd[$k] = $dur }
  if ($segEnd[$k] -lt $segStart[$k]) {
    throw "Adjustment too large near index=$k (start=$($segStart[$k]) end=$($segEnd[$k]))"
  }
}

$fc = @()
$fc += ("[0:a]aformat=sample_rates={0}:channel_layouts={1},asetpts=PTS-STARTPTS[a]" -f $sr, $cl)

$order = @()
for ($k = 0; $k -le $N; $k++) {
  $tag = ('seg{0:d3}' -f $k)
  $fc += ("[a]atrim={0}:{1},asetpts=PTS-STARTPTS[{2}]" -f (F $segStart[$k]), (F $segEnd[$k]), $tag)
  $order += ("[$tag]")

  if ($k -lt $N) {
    $delta = $items[$k].Delta
    if ($delta -lt 0) {
      $sTag = ('sil{0:d3}' -f $k)
      $insDur = [Math]::Abs($delta)
      if ($InsertMarker -eq 'sine') {
        $fc += ("sine=frequency={0}:sample_rate={1},atrim=0:{2},volume={3},aformat=sample_rates={1}:channel_layouts={4},asetpts=PTS-STARTPTS[{5}]" -f (F $MarkerFreqHz), $sr, (F $insDur), (F $MarkerVolume), $cl, $sTag)
      } else {
        $fc += ("anullsrc=r={0}:cl={1},atrim=0:{2},asetpts=PTS-STARTPTS[{3}]" -f $sr, $cl, (F $insDur), $sTag)
      }
      $order += ("[$sTag]")
    }
  }
}

$fc += ("{0}concat=n={1}:v=0:a=1[aout]" -f ($order -join ''), $order.Count)

$filter = ($fc -join ";`n")
WriteUtf8NoBom $filterScript $filter

Write-Host "WorkDir    : $workDir"
Write-Host "Input mp3  : $($mp3.Name)"
Write-Host "Adjust file: $adjFile"
Write-Host "Lines      : $N"
Write-Host "Filter     : $filterScript"
Write-Host "Output mp3 : $outMp3"

& ffmpeg -hide_banner -y -i $inMp3 -/filter_complex $filterScript -map "[aout]" -c:a libmp3lame -b:a 192k $outMp3

Write-Host "Merge video: $inVideo + subtitle.mp3 -> lights_out_audio.mp4"
& ffmpeg -hide_banner -y -i $inVideo -i $outMp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest $outVideo

$esc = { param($s) ($s -replace "'", "''") }
$helper = @()
$helper += '$ErrorActionPreference = "Stop"'
$helper += ("$workDir = '{0}'" -f (&$esc $workDir))
$helper += ("$inMp3 = '{0}'" -f (&$esc $inMp3))
$helper += ("$inVideo = '{0}'" -f (&$esc $inVideo))
$helper += ("$outMp3 = '{0}'" -f (&$esc $outMp3))
$helper += ("$outVideo = '{0}'" -f (&$esc $outVideo))
$helper += ("$filterScript = '{0}'" -f (&$esc $filterScript))
$helper += 'Set-Location $workDir'
$helper += 'ffmpeg -hide_banner -y -i "$inMp3" -/filter_complex "$filterScript" -map "[aout]" -c:a libmp3lame -b:a 192k "$outMp3"'
$helper += 'ffmpeg -hide_banner -y -i "$inVideo" -i "$outMp3" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest "$outVideo"'
WriteUtf8NoBom $helperPath ($helper -join "`r`n")

Write-Host "Helper script generated: $helperPath"
Write-Host 'Done.'
