@echo off
echo ========================================
echo TeBium Alert Bot - Push to GitHub
echo ========================================
echo.

echo Step 1: Navigate to project directory
cd /d "C:\Prodjects\TeBium-Alert-Bot"
echo Current directory: %CD%

echo.
echo Step 2: Check Git status
git status

echo.
echo Step 3: Remove existing remote (if any)
git remote remove origin 2>nul

echo Step 4: Add GitHub remote
git remote add origin https://github.com/TigranWQ/tebium-alert-bot.git

echo.
echo Step 5: Check remote repositories
git remote -v

echo.
echo Step 6: Rename branch to main
git branch -M main

echo.
echo Step 7: Push to GitHub
echo This may ask for your GitHub credentials...
git push -u origin main

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS! Code pushed to GitHub
    echo Repository: https://github.com/TigranWQ/tebium-alert-bot
) else (
    echo ERROR! Push failed. Check your credentials.
)
echo ========================================
echo.

pause
