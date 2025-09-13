@echo off
echo Setting up Git for TeBium Alert Bot...

cd /d "C:\Prodjects\TeBium-Alert-Bot"

echo Current directory:
cd

echo.
echo Checking Git status...
git status

echo.
echo Adding remote repository...
git remote add origin https://github.com/TigranWQ/tebium-alert-bot.git

echo.
echo Checking remote repositories...
git remote -v

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo Git setup completed!
echo Repository URL: https://github.com/TigranWQ/tebium-alert-bot

pause
