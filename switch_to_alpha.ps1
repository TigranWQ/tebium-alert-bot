# TeBium Alert Bot - Переход в ветку альфа

Write-Host "🌿 Переход в ветку альфа..." -ForegroundColor Green

# Переход в папку проекта
Set-Location "C:\Prodjects\TeBium-Alert-Bot"

Write-Host "📁 Текущая папка: $(Get-Location)" -ForegroundColor Yellow

# Проверка текущего статуса
Write-Host "🔍 Проверка текущего статуса Git..." -ForegroundColor Yellow
git status

# Создание и переход в ветку альфа
Write-Host "🌿 Создание и переход в ветку альфа..." -ForegroundColor Yellow
git checkout -b alpha

# Проверка текущей ветки
Write-Host "✅ Текущая ветка:" -ForegroundColor Green
git branch

# Отправка ветки на GitHub
Write-Host "📤 Отправка ветки альфа на GitHub..." -ForegroundColor Yellow
git push -u origin alpha

Write-Host "🎉 Успешно перешли в ветку альфа!" -ForegroundColor Green
Write-Host "🔗 Ветка доступна: https://github.com/TigranWQ/tebium-alert-bot/tree/alpha" -ForegroundColor Cyan

Read-Host "Нажмите Enter для продолжения"
