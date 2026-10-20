@echo off
setlocal EnableExtensions
title BIS Nirdesh - API Manager
cd /d "%~dp0"

echo.
echo ========================================================
echo              BIS NIRDESH API MANAGER
echo ========================================================
echo API keys are entered with hidden input and stored locally.
echo Add multiple keys to enable automatic failover.
echo.

where py >nul 2>nul
if not errorlevel 1 (
  set "PY_LAUNCH=py -3"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo ERROR: Python 3.10 or newer was not found.
    echo Install Python from https://www.python.org/downloads/
    goto :fail
  )
  set "PY_LAUNCH=python"
)

if not exist "backend\.venv\Scripts\python.exe" (
  echo Creating Python environment...
  %PY_LAUNCH% -m venv "backend\.venv"
  if errorlevel 1 goto :fail
)

echo Checking backend dependencies...
"backend\.venv\Scripts\python.exe" -m pip install -r "backend\requirements.txt"
if errorlevel 1 goto :fail

"backend\.venv\Scripts\python.exe" "backend\manage_api_keys.py"
set "RESULT=%ERRORLEVEL%"
echo.
if not "%RESULT%"=="0" (
  echo API Manager exited with an error.
  goto :fail
)
echo API Manager finished.
pause
exit /b 0

:fail
echo.
echo API Manager failed. Read the error above.
pause
exit /b 1
