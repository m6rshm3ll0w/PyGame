@echo off
(echo.set sh=CreateObject^("Wscript.Shell"^)
echo.sh.Run """%~nx0"" 1", 0)>launch.vbs
if "%~1"=="" (start "" "launch.vbs"&exit /b)


./venv/Scripts/python.exe main.py