@echo off
setlocal
chcp 65001 >nul
python "%~dp0harness.py" %*
endlocal
