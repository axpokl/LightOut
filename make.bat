del *.exe
for /f %%g in ('dir /b "diandeng*.pas"') do fpc "%%g" -gl -Crtoi -WG
del *.obj
del *.ppu
del *.o
del *.or
del *.a
pause