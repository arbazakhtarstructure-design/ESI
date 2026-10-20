@echo off
cd /d "%~dp0"
py -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
  echo Could not install build requirements.
  pause
  exit /b 1
)
py -m PyInstaller --noconfirm --clean --windowed --name FootingDesignPro app.py
if errorlevel 1 (
  echo Build failed. See messages above.
  pause
  exit /b 1
)
echo.
echo Build complete. EXE folder: dist\FootingDesignPro\
pause
