@echo off
echo ========================================
echo TeBium Alert Bot - Загрузка на GitHub
echo ========================================
echo.

echo Шаг 1: Переход в папку проекта
cd /d "C:\Prodjects\TeBium-Alert-Bot"
echo Текущая папка: %CD%

echo.
echo Шаг 2: Добавление всех файлов
git add .

echo.
echo Шаг 3: Создание коммита на русском языке
git commit -m "Первоначальный коммит: TeBium Alert Bot - Telegram бот для мониторинга системы и алертов

🚨 Функции:
- Полный Telegram бот для системных алертов и мониторинга
- Интеграция с модулями экосистемы TeBium
- Безопасная конфигурация с защитой токена
- Поддержка Docker контейнеризации
- Подробная документация и руководства по безопасности

🔗 Интеграция с экосистемой:
- TeBium-Analytics-Server: https://github.com/TigranWQ/tebium-analytics-server
- Telegram-Bot-Tebium: https://github.com/TigranWQ/telegram-bot-tebium
- TeBium-Alert-Bot: https://github.com/TigranWQ/tebium-alert-bot

🛡️ Безопасность:
- Токен бота: 8354021077:AAFKnwLGblJggn4qpgxnfnw4Msw8jsbTsMg
- Безопасная конфигурация в config.env (исключена из Git)
- Аутентификация webhook и ограничение скорости
- Подробная документация по безопасности

📚 Документация:
- README.md - Полная документация проекта
- SECURITY.md - Руководства и лучшие практики безопасности
- QUICK_START.md - Руководство по быстрому старту
- ARCHITECTURE.md - Обзор архитектуры системы
- ECOSYSTEM.md - Интеграция с экосистемой TeBium

🚀 Готов к развертыванию и интеграции с экосистемой TeBium!"

echo.
echo Шаг 4: Удаление существующего remote (если есть)
git remote remove origin 2>nul

echo Шаг 5: Добавление GitHub remote
git remote add origin https://github.com/TigranWQ/tebium-alert-bot.git

echo.
echo Шаг 6: Проверка remote репозиториев
git remote -v

echo.
echo Шаг 7: Переименование ветки в main
git branch -M main

echo.
echo Шаг 8: Загрузка на GitHub
echo Это может запросить ваши учетные данные GitHub...
git push -u origin main

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo УСПЕХ! Код загружен на GitHub
    echo Репозиторий: https://github.com/TigranWQ/tebium-alert-bot
) else (
    echo ОШИБКА! Загрузка не удалась. Проверьте ваши учетные данные.
)
echo ========================================
echo.

pause
