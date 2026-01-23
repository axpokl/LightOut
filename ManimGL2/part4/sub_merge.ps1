$ErrorActionPreference = 'Stop'

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw 'ffmpeg not found in PATH' }

$workDir = (Get-Location).Path
$videosDir = Join-Path $workDir 'videos'
if (-not (Test-Path -LiteralPath $videosDir)) { throw "Missing folder: $videosDir" }

$musicDir = Join-Path $workDir 'music'
if (-not (Test-Path -LiteralPath $musicDir)) { throw "Missing folder: $musicDir" }

$combineScript = Join-Path $musicDir 'combine.ps1'
if (-not (Test-Path -LiteralPath $combineScript)) { throw "Missing script: $combineScript" }

Write-Host "Run: $combineScript"
Push-Location $musicDir
& $combineScript
Pop-Location

$bgmMp3 = Join-Path $musicDir 'bgm.mp3'
if (-not (Test-Path -LiteralPath $bgmMp3)) { throw "Missing bgm mp3: $bgmMp3" }

$inVideo = Join-Path $videosDir 'lights_out.mp4'
if (-not (Test-Path -LiteralPath $inVideo)) { throw "Missing video: $inVideo" }

$outMp3 = Join-Path $videosDir 'subtitle.mp3'
if (-not (Test-Path -LiteralPath $outMp3)) { throw "Missing subtitle mp3: $outMp3" }

$combineMp3 = Join-Path $videosDir 'combine.mp3'
Write-Host "Mix audio: bgm.mp3 + subtitle.mp3 -> combine.mp3"
$bgmVolume = 0.25
& ffmpeg -hide_banner -y -i $bgmMp3 -i $outMp3 -filter_complex "[0:a]volume=$bgmVolume[bgm];[1:a]volume=1.0[sub];[bgm][sub]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,alimiter=limit=0.98[a]" -map "[a]" -c:a libmp3lame -b:a 192k $combineMp3

$outVideo = Join-Path $videosDir 'lights_out_audio.mp4'

Write-Host "Merge video: $inVideo + combine.mp3 -> lights_out_audio.mp4"
& ffmpeg -hide_banner -y -i $inVideo -i $combineMp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -af "apad" -shortest $outVideo

Write-Host 'Done.'
