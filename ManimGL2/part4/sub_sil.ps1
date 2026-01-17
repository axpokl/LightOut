param(
  [double]$MinSilenceSec = 0.5,
  [string]$NoiseDb = "-30dB",
  [string]$InputMp3,
  [switch]$IncludeTailSilence,
  [switch]$Debug = $True,
  [int]$DebugHeadEvents = 25
)

$ErrorActionPreference = 'Stop'
$inv = [System.Globalization.CultureInfo]::InvariantCulture
$BUILD = "2026-01-18-debug-v1"

function SecToTs([double]$sec) {
  if ($sec -lt 0) { $sec = 0 }
  $ms = [int64][Math]::Round($sec * 1000.0)
  $h = [int64]($ms / 3600000); $ms %= 3600000
  $m = [int64]($ms / 60000);   $ms %= 60000
  $s = [int64]($ms / 1000);    $ms %= 1000
  "{0:00}:{1:00}:{2:00}.{3:000}" -f $h, $m, $s, $ms
}

function WriteUtf8NoBom([string]$path, [string]$text) {
  $enc = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($path, $text, $enc)
}

function F([double]$x) { [string]::Format($inv, "{0:0.###}", $x) }

function RunNative([string]$exe, [string[]]$nativeArgs) {
  $oldEAP = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'

  $hadNative = $false
  $oldNative = $null
  if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -Scope Global -ErrorAction SilentlyContinue) {
    $hadNative = $true
    $oldNative = $global:PSNativeCommandUseErrorActionPreference
    $global:PSNativeCommandUseErrorActionPreference = $false
  }

  $out = & $exe @nativeArgs 2>&1
  $code = $LASTEXITCODE

  if ($hadNative) { $global:PSNativeCommandUseErrorActionPreference = $oldNative }
  $ErrorActionPreference = $oldEAP

  return @{ Code = $code; Out = $out }
}

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw "ffmpeg not found in PATH" }
if (-not (Get-Command ffprobe -ErrorAction SilentlyContinue)) { throw "ffprobe not found in PATH" }

$workDir = (Get-Location).Path
$outTxt  = Join-Path $workDir "sub_sil.txt"
$ffLog   = Join-Path $workDir "sub_sil_ffmpeg.log"
$evCsv   = Join-Path $workDir "sub_sil_events.csv"
$pairCsv = Join-Path $workDir "sub_sil_pairs.csv"

if ($InputMp3) {
  $inMp3 = (Resolve-Path -LiteralPath $InputMp3).Path
} else {
  $pick = Get-ChildItem -LiteralPath $workDir -File -Filter *.mp3 |
    Sort-Object Length -Descending |
    Select-Object -First 1
  if (-not $pick) { throw "No mp3 found in current directory: $workDir" }
  $inMp3 = $pick.FullName
}

if ($Debug) {
  Write-Host "=== DEBUG BUILD === $BUILD"
  Write-Host "PSCommandPath : $PSCommandPath"
  if ($PSCommandPath -and (Test-Path -LiteralPath $PSCommandPath)) {
    $si = Get-Item -LiteralPath $PSCommandPath
    $sh = Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256
    Write-Host ("Script File   : {0}  {1} bytes  {2}" -f $si.FullName, $si.Length, $si.LastWriteTime)
    Write-Host ("Script SHA256 : {0}" -f $sh.Hash)
  }
  $fi = Get-Item -LiteralPath $inMp3
  Write-Host ("Input Full    : {0}" -f $fi.FullName)
  Write-Host ("Input Size    : {0} bytes" -f $fi.Length)
  Write-Host ("Input Time    : {0}" -f $fi.LastWriteTime)
  Write-Host ""
}

$durR = RunNative "ffprobe" @(
  "-v","error",
  "-show_entries","format=duration",
  "-of","default=noprint_wrappers=1:nokey=1",
  $inMp3
)
if ($durR.Code -ne 0) {
  $tail = ($durR.Out | Select-Object -Last 60) -join "`n"
  throw "ffprobe failed with exit code $($durR.Code)`n$tail"
}
$durRaw = ($durR.Out | ForEach-Object { [string]$_ }) -join "`n"
$durLine = ($durR.Out | Where-Object { $_ -match '^[0-9]+(\.[0-9]+)?$' } | Select-Object -First 1)
if (-not $durLine) { throw "ffprobe duration parse failed`n$durRaw" }
$duration = [double]::Parse($durLine, $inv)

$filter = "silencedetect=noise=${NoiseDb}:d=$(F $MinSilenceSec)"

$ffArgs = @(
  "-hide_banner","-nostats",
  "-i",$inMp3,
  "-vn",
  "-af",$filter,
  "-f","null","-"
)

$r = RunNative "ffmpeg" $ffArgs
if ($r.Code -ne 0) {
  $tail = ($r.Out | Select-Object -Last 120) -join "`n"
  throw "ffmpeg failed with exit code $($r.Code)`n$tail"
}

$log = $r.Out | ForEach-Object { [string]$_ }

if ($Debug) {
  WriteUtf8NoBom $ffLog ($log -join "`r`n")
}

$ffHeaderDur = $null
foreach ($line in $log) {
  $m = [regex]::Match($line, 'Duration:\s*(?<h>\d+):(?<m>\d+):(?<s>\d+(?:\.\d+)?)')
  if ($m.Success) {
    $hh = [int]$m.Groups['h'].Value
    $mm = [int]$m.Groups['m'].Value
    $ss = [double]::Parse($m.Groups['s'].Value, $inv)
    $ffHeaderDur = ($hh * 3600.0) + ($mm * 60.0) + $ss
    break
  }
}

$segments = New-Object System.Collections.Generic.List[object]
$events   = New-Object System.Collections.Generic.List[object]
$pairs    = New-Object System.Collections.Generic.List[object]

$curStart = $null
$curStartIdx = $null
$idx = 0

$startOverwrite = 0
$endWithoutStart = 0
$reversePairs = 0

foreach ($line in $log) {
  $m1 = [regex]::Match($line, 'silence_start:\s*(?<t>-?\d+(?:\.\d+)?)')
  if ($m1.Success) {
    $idx++
    $t = [double]::Parse($m1.Groups['t'].Value, $inv)
    $events.Add([pscustomobject]@{ Idx=$idx; Kind="start"; T=$t; Dur=$null; Line=$line })
    if ($curStart -ne $null) { $startOverwrite++ }
    $curStart = $t
    $curStartIdx = $idx
    continue
  }

  $m2 = [regex]::Match($line, 'silence_end:\s*(?<t>-?\d+(?:\.\d+)?)(?:\s*\|\s*silence_duration:\s*(?<d>-?\d+(?:\.\d+)?))?')
  if ($m2.Success) {
    $idx++
    $end = [double]::Parse($m2.Groups['t'].Value, $inv)
    $d = $null
    if ($m2.Groups['d'].Success) { $d = [double]::Parse($m2.Groups['d'].Value, $inv) }
    $events.Add([pscustomobject]@{ Idx=$idx; Kind="end"; T=$end; Dur=$d; Line=$line })

    if ($curStart -eq $null) {
      $endWithoutStart++
      continue
    }

    $st = [double]$curStart
    $stIdx = $curStartIdx
    $curStart = $null
    $curStartIdx = $null

    $isReverse = $false
    if ($end -lt $st) { $isReverse = $true; $reversePairs++ }

    $calc = $end - $st
    $segments.Add([pscustomobject]@{ Start=$st; End=$end; StartIdx=$stIdx; EndIdx=$idx })
    $pairs.Add([pscustomobject]@{
      StartIdx=$stIdx; EndIdx=$idx;
      Start=$st; End=$end;
      CalcDur=$calc;
      DurField=$d;
      Reverse=$isReverse
    })
  }
}

if ($IncludeTailSilence -and $curStart -ne $null) {
  $segments.Add([pscustomobject]@{ Start=$curStart; End=$duration; StartIdx=$curStartIdx; EndIdx=$null })
  $pairs.Add([pscustomobject]@{
    StartIdx=$curStartIdx; EndIdx=$null;
    Start=$curStart; End=$duration;
    CalcDur=($duration-$curStart);
    DurField=$null;
    Reverse=$false
  })
}

$lines = foreach ($s in $segments) {
  "{0}`t{1}" -f (SecToTs $s.Start), (SecToTs $s.End)
}
WriteUtf8NoBom $outTxt ($lines -join "`r`n")

if ($Debug) {
  $evLines = @("Idx,Kind,T,DurField,Line")
  foreach ($e in $events) {
    $t = [string]::Format($inv, "{0:0.###}", [double]$e.T)
    $d = ""
    if ($e.Dur -ne $null) { $d = [string]::Format($inv, "{0:0.###}", [double]$e.Dur) }
    $ln = ($e.Line -replace '"','""')
    $evLines += ('{0},{1},{2},{3},"{4}"' -f $e.Idx, $e.Kind, $t, $d, $ln)
  }
  WriteUtf8NoBom $evCsv ($evLines -join "`r`n")

  $pairLines = @("StartIdx,EndIdx,Start,End,CalcDur,DurField,Reverse")
  foreach ($p in $pairs) {
    $df = ""
    if ($p.DurField -ne $null) { $df = [string]::Format($inv, "{0:0.###}", [double]$p.DurField) }
    $pairLines += ('{0},{1},{2},{3},{4},{5},{6}' -f
      $p.StartIdx,
      $p.EndIdx,
      [string]::Format($inv, "{0:0.###}", [double]$p.Start),
      [string]::Format($inv, "{0:0.###}", [double]$p.End),
      [string]::Format($inv, "{0:0.###}", [double]$p.CalcDur),
      $df,
      $p.Reverse
    )
  }
  WriteUtf8NoBom $pairCsv ($pairLines -join "`r`n")
}

Write-Host "Input : $(Split-Path -Leaf $inMp3)"
Write-Host "Dur   : $(SecToTs $duration) ($([string]::Format($inv,'{0:0.###}',$duration)) sec)"
if ($ffHeaderDur -ne $null) {
  Write-Host "FF Dur: $(SecToTs $ffHeaderDur) ($([string]::Format($inv,'{0:0.###}',$ffHeaderDur)) sec)"
}
Write-Host "Filter: $filter"
Write-Host "Output: $outTxt"
Write-Host "Found : $($segments.Count) silence segments"

if ($Debug) {
  Write-Host ""
  Write-Host "=== DEBUG: anomalies ==="
  Write-Host "ffprobe raw duration output:"
  Write-Host $durRaw
  Write-Host ""
  Write-Host ("events total           : {0}" -f $events.Count)
  Write-Host ("start overwrite count  : {0}" -f $startOverwrite)
  Write-Host ("end without start      : {0}" -f $endWithoutStart)
  Write-Host ("reverse pairs (end<st) : {0}" -f $reversePairs)

  $maxEnd = ($segments | Measure-Object End -Maximum).Maximum
  $minSt  = ($segments | Measure-Object Start -Minimum).Minimum
  Write-Host ("min start              : {0} ({1})" -f (SecToTs $minSt), [string]::Format($inv,'{0:0.###}',$minSt))
  Write-Host ("max end                : {0} ({1})" -f (SecToTs $maxEnd), [string]::Format($inv,'{0:0.###}',$maxEnd))

  Write-Host ""
  Write-Host "debug files:"
  Write-Host "  $ffLog"
  Write-Host "  $evCsv"
  Write-Host "  $pairCsv"
  Write-Host ""
  Write-Host "Head Events:"
  $events | Select-Object -First $DebugHeadEvents | ForEach-Object {
    $t = [string]::Format($inv,'{0:0.###}', [double]$_.T)
    if ($_.Kind -eq "start") {
      Write-Host ("  {0,4}  start  {1,10}  {2}" -f $_.Idx, $t, $_.Line)
    } else {
      $d = ""
      if ($_.Dur -ne $null) { $d = [string]::Format($inv,'{0:0.###}', [double]$_.Dur) }
      Write-Host ("  {0,4}  end    {1,10}  d={2}  {3}" -f $_.Idx, $t, $d, $_.Line)
    }
  }
}
