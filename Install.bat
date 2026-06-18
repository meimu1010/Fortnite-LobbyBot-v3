@echo off

if exist requirements.txt (
    py -m pip install -r requirements.txt
) else (
    echo requirements.txt が見つかりません。
)

pause