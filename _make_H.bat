@echo off
setlocal EnableDelayedExpansion

set /p START=<_make_range.txt
set END=0

for %%F in (diandeng10_a_faster2_png_H*.pas diandeng10_b_faster2_png_H*.pas) do (
	if exist "%%F" (
		for /f "tokens=5 delims=_" %%H in ("%%~nF") do (
			set "VER=%%H"
			set "VER=!VER:~1!"
			for /f "delims=0123456789" %%X in ("!VER!") do set "VER="
			if defined VER if !VER! GTR !END! set END=!VER!
	)
	)
)

if %END% LSS %START% (
	echo No H%START% or later source files found.
	exit /b 1
)

echo Range: H%START% - H%END%


for /L %%i in (%START%,1,%END%) do (
	if exist "diandeng10_a_faster2_png_H%%i.pas" fpc "diandeng10_a_faster2_png_H%%i.pas"
	if exist "diandeng10_a_faster2_png_H%%i_out.pas" fpc "diandeng10_a_faster2_png_H%%i_out.pas"
	if exist "diandeng10_b_faster2_png_H%%i.pas" fpc "diandeng10_b_faster2_png_H%%i.pas"
)

del /q *.obj 2>nul
del /q *.ppu 2>nul
del /q *.o 2>nul
del /q *.or 2>nul
del /q *.a 2>nul

endlocal
::pause