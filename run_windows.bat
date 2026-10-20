@echo off
cd /d "%~dp0"
py -m pip install -r requirements.txt
if errorlevel 1 (
  echo Could not install requirements. Check Python installation and internet connection.
  pause
  exit /b 1
)
py app.py
pause
