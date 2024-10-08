@echo off
setlocal EnableDelayedExpansion

:: 检查是否提供了参数
if "%~1"=="" (
    echo Usage: commit.bat ^<hours^>
    exit /b 1
)

:: 将小时数转换为秒数
set /a totalSeconds=%1*3600

:: 显示倒计时
echo.
echo Countdown to auto-commit...
echo.

:countdown
if %totalSeconds% gtr 0 (
    :: 计算剩余的小时数、分钟数和秒数
	set /a s=3600,m=60
    set /a hours=%totalSeconds% / %s%
    set /a minutes=%totalSeconds% %% %s% / %m%
    set /a seconds=%totalSeconds% %% %m%
    echo In %hours% hours, %minutes% minutes, and %seconds% seconds, auto-commit will start...
    timeout /t 1 /nobreak >nul
    set /a totalSeconds-=1
    goto countdown
) else (
    echo Auto-commit starting...
)

:: 检查当前目录是否为 Git 仓库
git rev-parse --is-inside-work-tree >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: This directory is not a Git repository.
    exit /b 1
)

:: 执行 Git 命令
echo Adding all changes...
git add .
if %errorlevel% neq 0 (
    echo Error: Failed to add changes.
    exit /b 1
)

echo Committing changes...
git commit -m "Fix some bug"
if %errorlevel% neq 0 (
    echo Error: Failed to commit changes.
    exit /b 1
)

echo Pushing changes...
git push
if %errorlevel% neq 0 (
    echo Error: Failed to push changes.
    exit /b 1
)

echo Done.
pause
exit /b 0
