@echo off

set /p SEARCH_TEXT=ŒŸõ•¶Žš—ñ‚ð“ü—Í‚µ‚Ä‚­‚¾‚³‚¢: 

if "%SEARCH_TEXT%"=="" (
    echo ŒŸõ•¶Žš—ñ‚ª“ü—Í‚³‚ê‚Ä‚¢‚Ü‚¹‚ñB
    pause
    exit /b
)

echo.
echo ŒŸõ’†...
findstr /s /n /i /c:"%SEARCH_TEXT%" *.*

echo.
echo ŒŸõI—¹
pause