del *.exe
for /f %%g in ('dir /b "diandeng*.pas"') do fpc "%%g" -ddisp
for /f %%g in ('dir /b "rcalc*.pas"') do fpc "%%g" -ddisp
del *.obj
del *.ppu
del *.o
del *.or
del *.a
pause
