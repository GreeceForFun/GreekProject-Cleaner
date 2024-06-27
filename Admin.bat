@echo off
:: Prompt for administrator privileges
NET FILE 1>NUL 2>NUL
if "%ERRORLEVEL%" == "0" (
    :: We have administrator privileges
    "python GreekProject.py"
) else (
    :: We don't have administrator privileges, so request elevation
    echo Requesting administrative privileges...
    powershell -Command "Start-Process 'python' -ArgumentList 'newgui.py' -Verb 'RunAs'"
)