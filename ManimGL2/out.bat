del subtitle.txt
del title.txt

manimgl lights_out_gl2.py LightsOutThreeGridsGL -w --file_name lights_out
if errorlevel 1 (
    pause
) else (
    start "" ".\videos\lights_out.mp4"
)
