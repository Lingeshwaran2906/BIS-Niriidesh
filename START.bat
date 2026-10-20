@echo off
setlocal EnableExtensions
title BIS Nirdesh - One Click Startup
cd /d "%~dp0"
color 0B

echo.
echo ========================================================
echo              BIS NIRDESH - STARTUP
echo ========================================================
echo Website   : http://127.0.0.1:5173
echo Backend   : http://127.0.0.1:8000
echo API docs  : http://127.0.0.1:8000/docs
echo.

where py >nul 2>nul
if not errorlevel 1 (
  set "PY_LAUNCH=py -3"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo ERROR: Python 3.10 or newer was not found.
    echo Install Python from https://www.python.org/downloads/ and enable PATH.
    goto :fail
  )
  set "PY_LAUNCH=python"
)

%PY_LAUNCH% -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)"
if errorlevel 1 (
  echo ERROR: Python 3.10 or newer is required.
  goto :fail
)

where node >nul 2>nul
if errorlevel 1 (
  echo ERROR: Node.js LTS was not found. Install it from https://nodejs.org/
  goto :fail
)
where npm >nul 2>nul
if errorlevel 1 (
  echo ERROR: npm was not found. Repair or reinstall Node.js LTS.
  goto :fail
)

if not exist "backend\.venv\Scripts\python.exe" (
  echo [1/6] Creating backend Python environment...
  %PY_LAUNCH% -m venv "backend\.venv"
  if errorlevel 1 goto :fail
) else (
  echo [1/6] Python environment found.
)

echo [2/6] Installing/checking backend dependencies...
"backend\.venv\Scripts\python.exe" -m pip install -r "backend\requirements.txt"
if errorlevel 1 goto :fail

echo [3/6] Creating local app configuration...
"backend\.venv\Scripts\python.exe" "backend\manage_api_keys.py" --ensure-config
if errorlevel 1 goto :fail

echo [4/6] Checking API key manager...
"backend\.venv\Scripts\python.exe" "backend\manage_api_keys.py" --has-keys
if errorlevel 1 (
  echo No Gemini API key is configured yet.
  call "%~dp0API_MANAGER.bat"
  if errorlevel 1 goto :fail
  "backend\.venv\Scripts\python.exe" "backend\manage_api_keys.py" --has-keys
  if errorlevel 1 (
    echo ERROR: No API key was saved. Use API_MANAGER.bat and add a key.
    goto :fail
  )
) else (
  echo Saved API keys found.
)

if not exist "frontend\package.json" (
  echo ERROR: frontend\package.json is missing.
  goto :fail
)
if not exist "frontend\node_modules" (
  echo [5/6] Installing frontend dependencies. This can take a few minutes...
  pushd "%~dp0frontend"
  call npm install
  if errorlevel 1 (
    popd
    goto :fail
  )
  popd
) else (
  echo [5/6] Frontend dependencies already installed.
)

echo [6/6] Starting backend and frontend...
echo.
rem Directly start Python in its own console; no nested batch-file quoting.
start "BIS Nirdesh Backend - port 8000" /D "%~dp0backend" "%~dp0backend\.venv\Scripts\python.exe" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
timeout /t 2 /nobreak >nul
rem npm is a cmd shim, so run it through cmd.exe with a simple command.
start "BIS Nirdesh Frontend - port 5173" /D "%~dp0frontend" "%ComSpec%" /k "npm run dev -- --host 127.0.0.1 --port 5173"
timeout /t 4 /nobreak >nul
start "" "http://127.0.0.1:5173"

echo.
echo ========================================================
echo Startup commands sent.
echo Website  : http://127.0.0.1:5173
echo Backend  : http://127.0.0.1:8000
echo API docs : http://127.0.0.1:8000/docs
echo Keep both server windows open while using BIS Nirdesh.
echo Use API_MANAGER.bat to add, test, switch, or remove keys.
echo ========================================================
echo.
pause
exit /b 0

:fail
echo.
echo ========================================================
echo STARTUP FAILED. Read the error above.
echo No terminal window will be hidden; press a key to close.
echo ========================================================
pause
exit /b 1
