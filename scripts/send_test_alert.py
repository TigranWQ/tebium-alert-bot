#!/usr/bin/env python3
"""
Скрипт для отправки тестового алерта
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Добавляем корневую папку в путь
sys.path.append(str(Path(__file__).parent.parent))

from utils.alert_manager import AlertManager
from utils.database import DatabaseManager
from config.settings import Settings

async def send_test_alert():
    """Отправка тестового алерта"""
    try:
        settings = Settings()
        db = DatabaseManager(settings.DATABASE_URL)
        
        # Инициализация базы данных
        await db.init_database()
        
        # Создание тестового алерта
        test_alert = {
            "type": "test",
            "message": "Это тестовое сообщение от скрипта",
            "priority": "info",
            "module": "TeBium-Alert-Bot",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "test": True,
                "script": "send_test_alert.py",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Сохранение алерта
        alert_id = await db.save_alert(test_alert)
        print(f"✅ Тестовый алерт создан: {alert_id}")
        
        # Вывод информации об алерте
        print(f"📋 Детали алерта:")
        print(f"   Тип: {test_alert['type']}")
        print(f"   Приоритет: {test_alert['priority']}")
        print(f"   Модуль: {test_alert['module']}")
        print(f"   Сообщение: {test_alert['message']}")
        print(f"   Время: {test_alert['timestamp']}")
        
    except Exception as e:
        print(f"❌ Ошибка отправки тестового алерта: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(send_test_alert())
