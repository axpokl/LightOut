param(
  [double]$MinSilenceSec = 0.5,
  [string]$NoiseDb = "-30dB",
  [string]$InputMp3,
  [switch]$IncludeTailSilence
)

$ErrorActionPreference = 'Stop'
$inv = [System.Globalization.CultureInfo]::InvariantCulture

function SecToTs([double]$sec) {
  if ($sec -lt 0) { $sec = 0 }
  $ms = [int][Math]::Round($sec * 1000.0)
  $h = [int]($ms / 3600000); $ms %= 3600000
  $m = [int]($ms / 60000);   $ms %= 60000
  $s = [int]($ms / 1000);    $ms %= 1000
  "{0:00}:{1:00}:{2:00}.{3:000}" -f $h, $m, $s, $ms
}

function WriteUtf8NoBom([string]$path, [string]$text) {
  $enc = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($path, $text, $enc)
}

function F([double]$x) {
  [string]::Format($inv, "{0:0.###}", $x)
}

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
$outTxt = Join-Path $workDir "sub_sil.txt"

if ($InputMp3) {
  $inMp3 = (Resolve-Path -LiteralPath $InputMp3).Path
} else {
  $pick = Get-ChildItem -LiteralPath $workDir -File -Filter *.mp3 |
    Sort-Object Length -Descending |
    Select-Object -First 1
  if (-not $pick) { throw "No mp3 found in current directory: $workDir" }
  $inMp3 = $pick.FullName
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
$durLine = ($durR.Out | Where-Object { $_ -match '^[0-9]+(\.[0-9]+)?$' } | Select-Object -First 1)
if (-not $durLine) { throw "ffprobe duration parse failed" }
$duration = [double]::Parse($durLine, $inv)

# 关键修复：冒号紧跟变量名时，PowerShell 可能会把 $NoiseDb:d 当成一个整体变量名
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

$log = $r.Out
$segments = New-Object System.Collections.Generic.List[object]
$curStart = $null

foreach ($line in $log) {
  $m1 = [regex]::Match($line, 'silence_start:\s*(?<t>-?\d+(?:\.\d+)?)')
  if ($m1.Success) {
    $curStart = [double]::Parse($m1.Groups['t'].Value, $inv)
    continue
  }

  $m2 = [regex]::Match($line, 'silence_end:\s*(?<t>-?\d+(?:\.\d+)?)(?:\s*\|\s*silence_duration:\s*(?<d>-?\d+(?:\.\d+)?))?')
  if ($m2.Success) {
    $end = [double]::Parse($m2.Groups['t'].Value, $inv)
    $d = $null
    if ($m2.Groups['d'].Success) { $d = [double]::Parse($m2.Groups['d'].Value, $inv) }

    if ($curStart -ne $null) {
      if (($d -eq $null) -or ($d -ge $MinSilenceSec - 1e-6)) {
        $segments.Add([pscustomobject]@{ Start = $curStart; End = $end })
      }
    }
    $curStart = $null
  }
}

if ($IncludeTailSilence -and $curStart -ne $null) {
  if ($duration -ge $curStart + $MinSilenceSec - 1e-6) {
    $segments.Add([pscustomobject]@{ Start = $curStart; End = $duration })
  }
}

$lines = foreach ($s in $segments) {
  "{0}`t{1}" -f (SecToTs $s.Start), (SecToTs $s.End)
}

WriteUtf8NoBom $outTxt ($lines -join "`r`n")

Write-Host "Input : $(Split-Path -Leaf $inMp3)"
Write-Host "Filter: $filter"
Write-Host "Output: $outTxt"
Write-Host "Found : $($segments.Count) silence segments"
