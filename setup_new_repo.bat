@echo off
echo ========================================
echo TeBium Alert Bot - Git Setup
echo ========================================
echo.

echo Step 1: Navigate to project directory
cd /d "C:\Prodjects\TeBium-Alert-Bot"

echo Step 2: Check Git status
git status

echo.
echo Step 3: Remove existing remote (if any)
git remote remove origin 2>nul

echo Step 4: Add new remote repository
git remote add origin https://github.com/TigranWQ/tebium-alert-bot.git

echo Step 5: Check remote repositories
git remote -v

echo.
echo Step 6: Rename branch to main
git branch -M main

echo.
echo Step 7: Push to GitHub
git push -u origin main

echo.
echo ========================================
echo Setup completed!
echo Repository: https://github.com/TigranWQ/tebium-alert-bot
echo ========================================
echo.

pause
