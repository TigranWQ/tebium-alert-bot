@echo off
echo Starting TeBium Alert Bot...

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found!
    pause
    exit /b 1
)

REM Проверка наличия виртуального окружения
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Активация виртуального окружения
call venv\Scripts\activate.bat

REM Установка зависимостей
echo Installing dependencies...
pip install -r requirements.txt

REM Создание необходимых папок
if not exist "data" mkdir data
if not exist "logs" mkdir logs

REM Запуск бота
echo Starting bot...
python alert_bot.py

pause
