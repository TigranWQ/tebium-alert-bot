# TeBium Alert Bot - Git Setup
# Execute this script to set up Git repository

$ErrorActionPreference = "Stop"

try {
    Write-Host "🚀 Setting up Git for TeBium Alert Bot..." -ForegroundColor Green
    
    # Change to project directory
    Set-Location "C:\Prodjects\TeBium-Alert-Bot"
    Write-Host "📁 Working directory: $(Get-Location)" -ForegroundColor Yellow
    
    # Check if we're in a git repository
    if (Test-Path ".git") {
        Write-Host "✅ Git repository found" -ForegroundColor Green
        
        # Check current status
        Write-Host "🔍 Git status:" -ForegroundColor Yellow
        git status --short
        
        # Add remote if not exists
        $remotes = git remote
        if ($remotes -notcontains "origin") {
            Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
            git remote add origin https://github.com/TigranWQ/tebium-alert-bot.git
        } else {
            Write-Host "✅ Remote 'origin' already exists" -ForegroundColor Green
        }
        
        # Show remotes
        Write-Host "📡 Remote repositories:" -ForegroundColor Yellow
        git remote -v
        
        # Rename branch to main
        Write-Host "🌿 Setting branch to main..." -ForegroundColor Yellow
        git branch -M main
        
        # Push to GitHub
        Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
        git push -u origin main
        
        Write-Host "🎉 Git setup completed successfully!" -ForegroundColor Green
        Write-Host "🔗 Repository: https://github.com/TigranWQ/tebium-alert-bot" -ForegroundColor Cyan
        
    } else {
        Write-Host "❌ Not a Git repository. Please run 'git init' first." -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please check your Git configuration and try again." -ForegroundColor Yellow
}

Read-Host "Press Enter to continue"
