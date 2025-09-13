#!/usr/bin/env python3
"""
Скрипт запуска TeBium Alert Bot
"""

import asyncio
import sys
import os
from pathlib import Path

# Добавляем корневую папку в путь
sys.path.append(str(Path(__file__).parent.parent))

from alert_bot import TeBiumAlertBot
from utils.logger import setup_logging

async def main():
    """Главная функция запуска"""
    logger = setup_logging()
    
    try:
        logger.info("🚀 Запуск TeBium Alert Bot...")
        
        # Создание экземпляра бота
        bot = TeBiumAlertBot()
        
        # Запуск в режиме polling
        await bot.start_polling()
        
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал остановки")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
