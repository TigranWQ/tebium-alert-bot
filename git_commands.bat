@echo off
echo Setting up Git repository for TeBium Alert Bot...

REM Add remote repository
git remote add origin https://github.com/TigranWQ/tebium-alert-bot.git

REM Check remote
git remote -v

REM Push to main branch
git branch -M main
git push -u origin main

echo Done! Repository is now connected to GitHub.
pause
