@echo off
REM Construit Misahondrahondra.exe avec PyInstaller
REM Usage : double-cliquer, ou lancer depuis un terminal Windows

pip install -r requirements.txt
pip install pyinstaller

pyinstaller --onefile --noconsole ^
    --name Misahondrahondra ^
    --add-data "misahondrahondra.mp3;." ^
    misahondrahondra.py

echo.
echo Termine. L'executable se trouve dans dist\Misahondrahondra.exe
echo N'oublie pas de placer misahondrahondra.mp3 a cote de l'exe si tu ne l'as pas embarque.
pause
