# TeBium Alert Bot - PowerShell скрипт запуска

Write-Host "🚀 Starting TeBium Alert Bot..." -ForegroundColor Green

# Проверка наличия Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ and try again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Проверка наличия виртуального окружения
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Активация виртуального окружения
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Установка зависимостей
Write-Host "📚 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Создание необходимых папок
$folders = @("data", "logs")
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder
        Write-Host "📁 Created folder: $folder" -ForegroundColor Green
    }
}

# Проверка конфигурации
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Please copy env.example to .env and configure it." -ForegroundColor Yellow
}

# Запуск бота
Write-Host "🚀 Starting bot..." -ForegroundColor Green
try {
    # Используем безопасный запуск
    python scripts/secure_start.py
} catch {
    Write-Host "❌ Error starting bot: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🛑 Bot stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
