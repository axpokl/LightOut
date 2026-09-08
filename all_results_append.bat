@echo off
setlocal EnableDelayedExpansion

set /p START=<_make_range.txt
set END=0

powershell -NoProfile -ExecutionPolicy Bypass -File ".\all_results_clear.ps1"

for %%F in (diandeng10_a_faster2_png_H*.exe diandeng10_b_faster2_png_H*.exe) do (
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
	echo No H%START% or later executable files found.
	exit /b 1
)

echo Range: H%START% - H%END%

for /L %%i in (%START%,1,%END%) do (
	if exist "diandeng10_b_faster2_png_H%%i.exe" (
		echo Executing diandeng10_b_faster2_png_H%%i.exe
		echo ===== diandeng10_b_faster2_png_H%%i.exe =====>>all_results_b.txt
		".\diandeng10_b_faster2_png_H%%i.exe">>all_results_b.txt 2>&1
		echo.>>all_results_b.txt
	)
)

for /L %%i in (%START%,1,%END%) do (
	if exist "diandeng10_a_faster2_png_H%%i.exe" (
		echo Executing diandeng10_a_faster2_png_H%%i.exe
		echo ===== diandeng10_a_faster2_png_H%%i.exe =====>>all_results_a.txt
		".\diandeng10_a_faster2_png_H%%i.exe">>all_results_a.txt 2>&1
		echo.>>all_results_a.txt
	)
)

powershell -NoProfile -ExecutionPolicy Bypass -File ".\all_results_calc.ps1"

endlocal