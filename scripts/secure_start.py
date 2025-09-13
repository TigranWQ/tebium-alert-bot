#!/usr/bin/env python3
"""
Безопасный запуск TeBium Alert Bot
"""

import os
import sys
import stat
import secrets
import string
from pathlib import Path

def generate_webhook_secret(length=32):
    """Генерация безопасного webhook секрета"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def check_security():
    """Проверка настроек безопасности"""
    print("🔒 Проверка безопасности...")
    
    # Проверка наличия config.env
    if not Path("config.env").exists():
        print("❌ Файл config.env не найден!")
        return False
    
    # Проверка прав доступа к config.env
    config_path = Path("config.env")
    file_mode = config_path.stat().st_mode
    if file_mode & stat.S_IROTH or file_mode & stat.S_IWOTH:
        print("⚠️  Предупреждение: config.env доступен другим пользователям!")
        print("   Рекомендуется: chmod 600 config.env")
    
    # Проверка наличия .gitignore
    if not Path(".gitignore").exists():
        print("❌ Файл .gitignore не найден!")
        return False
    
    # Проверка, что config.env в .gitignore
    with open(".gitignore", "r") as f:
        gitignore_content = f.read()
        if "config.env" not in gitignore_content:
            print("⚠️  Предупреждение: config.env не добавлен в .gitignore!")
    
    print("✅ Проверка безопасности завершена")
    return True

def setup_environment():
    """Настройка окружения"""
    print("⚙️  Настройка окружения...")
    
    # Создание необходимых папок
    folders = ["data", "logs", "backups"]
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        # Установка правильных прав доступа
        os.chmod(folder, 0o700)
        print(f"📁 Создана папка: {folder}")
    
    # Генерация webhook секрета если нужно
    config_path = Path("config.env")
    if config_path.exists():
        with open(config_path, "r") as f:
            content = f.read()
            if "WEBHOOK_SECRET=tebium_alert_webhook_2024_secure_key" in content:
                new_secret = generate_webhook_secret()
                content = content.replace(
                    "WEBHOOK_SECRET=tebium_alert_webhook_2024_secure_key",
                    f"WEBHOOK_SECRET={new_secret}"
                )
                with open(config_path, "w") as f:
                    f.write(content)
                print(f"🔑 Сгенерирован новый webhook секрет: {new_secret[:8]}...")
    
    print("✅ Окружение настроено")

def validate_config():
    """Валидация конфигурации"""
    print("🔍 Валидация конфигурации...")
    
    try:
        from config.settings import Settings
        settings = Settings()
        
        # Проверка обязательных параметров
        if not settings.BOT_TOKEN:
            print("❌ BOT_TOKEN не установлен!")
            return False
        
        if not settings.WEBHOOK_SECRET:
            print("❌ WEBHOOK_SECRET не установлен!")
            return False
        
        if settings.WEBHOOK_SECRET == "your-secret-key":
            print("⚠️  Используется стандартный webhook секрет!")
            print("   Рекомендуется изменить WEBHOOK_SECRET")
        
        print("✅ Конфигурация валидна")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка валидации: {e}")
        return False

def main():
    """Главная функция"""
    print("🚀 Безопасный запуск TeBium Alert Bot")
    print("=" * 50)
    
    # Проверка безопасности
    if not check_security():
        print("❌ Проверка безопасности не пройдена!")
        sys.exit(1)
    
    # Настройка окружения
    setup_environment()
    
    # Валидация конфигурации
    if not validate_config():
        print("❌ Валидация конфигурации не пройдена!")
        sys.exit(1)
    
    print("✅ Все проверки пройдены!")
    print("🚀 Запуск бота...")
    
    # Запуск бота
    try:
        from alert_bot import main as bot_main
        import asyncio
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
