@echo off
echo =============================================
echo   Compiling prank scripts to .exe files
echo =============================================
echo.

where pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
echo Compiling broken_screen.py...
pyinstaller --onefile --noconsole --name "broken_screen" broken_screen.py

echo.
echo Compiling error_storm.py...
pyinstaller --onefile --noconsole --name "error_storm" error_storm.py

echo.
echo Compiling fake_update.py...
pyinstaller --onefile --noconsole --name "fake_update" fake_update.py

echo.
echo Compiling mouse_chaos.py...
pyinstaller --onefile --noconsole --name "mouse_chaos" mouse_chaos.py

echo.
echo Compiling virus_prank.py...
pyinstaller --onefile --noconsole --name "virus_prank" virus_prank.py

echo.
echo =============================================
echo   Done! .exe files are in the dist\ folder
echo =============================================
pause
