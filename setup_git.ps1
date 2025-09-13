# TeBium Alert Bot - Git Setup Script

Write-Host "🚀 Setting up Git for TeBium Alert Bot..." -ForegroundColor Green

# Navigate to the project directory
Set-Location "C:\Prodjects\TeBium-Alert-Bot"

Write-Host "📁 Current directory: $(Get-Location)" -ForegroundColor Yellow

# Check Git status
Write-Host "🔍 Checking Git status..." -ForegroundColor Yellow
git status

# Add remote repository
Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
git remote add origin https://github.com/TigranWQ/tebium-alert-bot.git

# Check if remote was added
Write-Host "✅ Remote repositories:" -ForegroundColor Green
git remote -v

# Rename branch to main
Write-Host "🌿 Renaming branch to main..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host "🎉 Git setup completed successfully!" -ForegroundColor Green
Write-Host "🔗 Repository URL: https://github.com/TigranWQ/tebium-alert-bot" -ForegroundColor Cyan

Read-Host "Press Enter to continue"
