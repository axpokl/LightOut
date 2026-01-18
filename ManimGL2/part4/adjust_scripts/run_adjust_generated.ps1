$ErrorActionPreference = "Stop"
G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4 = 'G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4'
G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\1768716253906.mp3 = 'G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\1768716253906.mp3'
G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\videos\lights_out.mp4 = 'G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\videos\lights_out.mp4'
G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\videos\subtitle.mp3 = 'G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\videos\subtitle.mp3'
G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\videos\lights_out_audio.mp4 = 'G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\videos\lights_out_audio.mp4'
G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\adjust_scripts\filter_complex.txt = 'G:\Program Files\First Publisher\bin\i386-win32\pas\数学问题\diandeng\ManimGL2\part4\adjust_scripts\filter_complex.txt'
Set-Location $workDir
ffmpeg -hide_banner -y -i "$inMp3" -/filter_complex "$filterScript" -map "[aout]" -c:a libmp3lame -b:a 192k "$outMp3"
ffmpeg -hide_banner -y -i "$inVideo" -i "$outMp3" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest "$outVideo"