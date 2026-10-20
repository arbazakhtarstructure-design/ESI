# Footing Design Pro — Starter Desktop App

## What this version does
- Windows desktop interface built with Python + PyQt6
- Five footing type selectors:
  1. Isolated Plan Footing
  2. Isolated Sloped Footing
  3. Isolated Eccentric Footing
  4. Combined Footing
  5. Combined Eccentric Footing
- Input forms, schematic drawing panel, preliminary area and bearing-pressure summaries
- Save/open project as JSON
- Export calculation summary as TXT
- Windows launch and PyInstaller packaging scripts

## Important engineering limitation
This is a **starter/MVP interface**, not a complete structural design program. It currently performs preliminary area / bearing-pressure checks only. It does NOT automatically complete or certify footing flexure, one-way shear, punching shear, development length, dowels, settlement, full combined-footing pressure diagrams, reinforcement detailing, or all eccentric partial-contact cases. It is not for construction use without a complete independently checked design.

The diagrams are schematic and not to scale. Inputs and outputs should be independently checked against the applicable IS 456 provisions and geotechnical recommendations.

## Run on Windows
1. Install a supported Python 3 version from python.org and ensure Python is added to PATH.
2. Extract this ZIP to a folder.
3. Double-click `run_windows.bat`.
   - It installs PyQt6 and launches the app.
   - Alternatively, open Command Prompt in the folder and run:
     `py -m pip install -r requirements.txt`
     `py app.py`

## Build a Windows EXE
1. Run `build_exe_windows.bat`.
2. After a successful build, find the packaged app under `dist\FootingDesignPro\FootingDesignPro.exe`.
3. The first build requires internet access to install PyInstaller and dependencies.

## Project file
Use Open Project / Save Project to save a `.json` project file. This stores the input values and last displayed result text.
