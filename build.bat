@echo off
setlocal enabledelayedexpansion
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
cd /d "%ROOT%"

set "DICT_REPO_URL=https://github.com/pymlex/oxford-dictionary-parser.git"
set "GUI_REPO_URL=https://github.com/pymlex/unichat-gui.git"

if not exist "%ROOT%\oxford-dictionary-parser\" (
    git clone "%DICT_REPO_URL%" "%ROOT%\oxford-dictionary-parser"
)
if not exist "%ROOT%\unichat-gui\" (
    git clone "%GUI_REPO_URL%" "%ROOT%\unichat-gui"
)

call :install "%ROOT%\oxford-dictionary-parser"
call :install "%ROOT%"
call :install "%ROOT%\unichat-gui"

(
echo @echo off
echo start "" "%%~dp0\oxford-dictionary-parser\run_server.bat"
echo start "" "%%~dp0\run_server.bat"
echo start "" "%%~dp0\unichat-gui\run_server.bat"
echo start "" "http://127.0.0.1:8003/"
) > "%ROOT%\run_all.bat"

(
echo @echo off
echo cd /d "%%~dp0"
echo call ".venv\Scripts\activate.bat"
echo python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
echo pause
) > "%ROOT%\run_server.bat"

if exist "%ROOT%\oxford-dictionary-parser\" (
    (
    echo @echo off
    echo cd /d "%%~dp0"
    echo call ".venv\Scripts\activate.bat"
    echo python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
    echo pause
    ) > "%ROOT%\oxford-dictionary-parser\run_server.bat"
)

if exist "%ROOT%\unichat-gui\" (
    (
    echo @echo off
    echo cd /d "%%~dp0"
    echo call ".venv\Scripts\activate.bat"
    echo python -m uvicorn app.main:app --host 127.0.0.1 --port 8003
    echo start "" "http://127.0.0.1:8003/"
    echo pause
    ) > "%ROOT%\unichat-gui\run_server.bat"
)

powershell -NoProfile -Command ^
"$s=(New-Object -COM WScript.Shell).CreateShortcut('%ROOT%\\StartChat.lnk');" ^
"$s.TargetPath='%ROOT%\\run_all.bat';" ^
"$s.WorkingDirectory='%ROOT%';" ^
"$s.IconLocation='%SystemRoot%\\system32\\SHELL32.dll,1';" ^
"$s.Save();"

exit /b 0

:install
set "P=%~1"
if "%P%"=="" exit /b 0
if not exist "%P%\" exit /b 0
pushd "%P%"
if exist "setup.bat" (
    call setup.bat
) else (
    if not exist ".venv\Scripts\activate.bat" (
        python -m venv .venv
    )
    call .venv\Scripts\activate.bat
    if exist "requirements.txt" (
        .venv\Scripts\pip.exe install --upgrade pip
        .venv\Scripts\pip.exe install -r requirements.txt
    )
)
popd
exit /b 0