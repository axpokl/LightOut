ffmpeg ^
 -i "bgmusic\a.mp3" -i "bgmusic\b.mp3" -i "bgmusic\c.mp3" ^
 -i "bgmusic\d.mp3" -i "bgmusic\x.mp3" -i "bgmusic\y.mp3" -i "bgmusic\z.mp3" ^
 -filter_complex "[0:a]adelay=615800:all=1[a];[1:a]adelay=829900:all=1[b];[2:a]adelay=157000:all=1[c];[3:a]adelay=0:all=1[d];[4:a]adelay=259200:all=1[x];[5:a]adelay=553700:all=1[y];[6:a]adelay=936100:all=1[z];[a][b][c][d][x][y][z]amix=inputs=7:duration=longest:normalize=0,alimiter=limit=0.97[out]" ^
 -map "[out]" -ar 48000 -ac 2 -c:a libmp3lame -b:a 192k "拼接.mp3"

ffmpeg -i "插空.mp3" -af "adelay=19000:all=1" -ar 48000 -ac 2 -c:a libmp3lame -b:a 192k "插空完整.mp3"

ffmpeg ^
 -i "拼接.mp3" ^
 -i "插空完整.mp3" ^
 -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest[out]" ^
 -map "[out]" ^
 -ar 48000 ^
 -ac 2 ^
 -c:a libmp3lame ^
 -b:a 192k ^
 "合并.mp3"

ffmpeg ^
 -i "videos\lights_out.mp4" ^
 -i ".\合并.mp3" ^
 -map 0:v:0 ^
 -map 1:a:0 ^
 -c:v copy ^
 -c:a aac ^
 -ar 48000 ^
 -ac 2 ^
 -movflags +faststart ^
 -shortest ^
 "videos\lights_out_with_audio.mp4"

pause