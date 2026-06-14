@echo off
color 07

where python > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install it before running this script. 1>&2
    exit /b
)

if not exist requirements.txt (
    echo The requirements.txt file doesn't exist, please make sure you have all the FortniteLobbyBot files. 1>&2
    exit /b
)

if exist .\local (
    echo Skipping 'pip install -r requirements.txt' as .local folder exists.
    echo This message is displayed in yellow.
) else (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo There was an error installing the requirements. Please check your Python installation and the contents of requirements.txt. 1>&2
        exit /b
    )
    echo Requirements installed correctly!
)

set /p version_choice=Do you want to use the 'main' or 'dev' version to start the bot? (Type 'main' or 'dev' and press Enter): 
if /i "%version_choice%" equ "dev" (
    python index.py -dev -use-device-auth -use-authorization-code
) else (
    python index.py -use-device-auth -use-authorization-code
)
if %errorlevel% neq 0 (
    echo There was an error running the bot. Please check your Python installation and the FortniteLobbyBot files. 1>&2
)

pause >nul
