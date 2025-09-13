#!/usr/bin/env python3
"""
TeBium Alert Bot - Модуль для отправки системных уведомлений и алертов
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import aiohttp
import json
import sqlite3
from datetime import datetime
import os

# Добавляем корневую папку в путь для импортов
sys.path.append(str(Path(__file__).parent))

from config.settings import Settings
from utils.database import DatabaseManager
from utils.alert_manager import AlertManager
from utils.logger import setup_logging
from handlers import register_handlers

# Настройка логирования
logger = setup_logging()

class TeBiumAlertBot:
    """Основной класс бота для отправки алертов"""
    
    def __init__(self):
        self.settings = Settings()
        self.bot = Bot(token=self.settings.BOT_TOKEN)
        self.dp = Dispatcher()
        self.db = DatabaseManager(self.settings.DATABASE_URL)
        self.alert_manager = AlertManager(self.bot, self.db)
        
        # Регистрируем обработчики
        register_handlers(self.dp, self.alert_manager)
        
        # Webhook URL для получения алертов от других модулей
        self.webhook_url = f"/webhook/{self.settings.WEBHOOK_SECRET}"
        
    async def start_polling(self):
        """Запуск бота в режиме polling"""
        try:
            logger.info("🚀 Запуск TeBium Alert Bot в режиме polling...")
            
            # Инициализация базы данных
            await self.db.init_database()
            
            # Запуск бота
            await self.dp.start_polling(self.bot)
            
        except Exception as e:
            logger.error(f"❌ Ошибка при запуске бота: {e}")
            raise
    
    async def start_webhook(self, webhook_url: str, webhook_path: str):
        """Запуск бота в режиме webhook"""
        try:
            logger.info(f"🚀 Запуск TeBium Alert Bot в режиме webhook: {webhook_url}")
            
            # Инициализация базы данных
            await self.db.init_database()
            
            # Установка webhook
            await self.bot.set_webhook(
                url=webhook_url,
                secret_token=self.settings.WEBHOOK_SECRET
            )
            
            # Настройка webhook сервера
            app = web.Application()
            webhook_requests_handler = SimpleRequestHandler(
                dispatcher=self.dp,
                bot=self.bot,
                secret_token=self.settings.WEBHOOK_SECRET
            )
            webhook_requests_handler.register(app, path=webhook_path)
            setup_application(app, self.dp, bot=self.bot)
            
            # Добавляем endpoint для получения алертов
            app.router.add_post(self.webhook_url, self.handle_alert_webhook)
            
            # Запуск сервера
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', self.settings.WEBHOOK_PORT)
            await site.start()
            
            logger.info(f"✅ Webhook сервер запущен на порту {self.settings.WEBHOOK_PORT}")
            
            # Держим сервер запущенным
            try:
                await asyncio.Future()  # Запуск навсегда
            except KeyboardInterrupt:
                logger.info("🛑 Получен сигнал остановки")
            finally:
                await runner.cleanup()
                
        except Exception as e:
            logger.error(f"❌ Ошибка при запуске webhook: {e}")
            raise
    
    async def handle_alert_webhook(self, request):
        """Обработка входящих алертов через webhook"""
        try:
            # Проверка секретного токена
            if request.headers.get('Authorization') != f"Bearer {self.settings.WEBHOOK_SECRET}":
                return web.Response(status=401, text="Unauthorized")
            
            # Получение данных алерта
            data = await request.json()
            logger.info(f"📨 Получен алерт: {data.get('type', 'unknown')}")
            
            # Обработка алерта
            await self.alert_manager.process_alert(data)
            
            return web.Response(status=200, text="OK")
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки webhook: {e}")
            return web.Response(status=500, text="Internal Server Error")
    
    async def send_system_alert(self, alert_type: str, message: str, 
                              priority: str = "info", module: str = "system",
                              data: Optional[Dict] = None):
        """Отправка системного алерта"""
        alert_data = {
            "type": alert_type,
            "message": message,
            "priority": priority,
            "module": module,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        await self.alert_manager.process_alert(alert_data)
    
    async def get_alert_history(self, limit: int = 50) -> List[Dict]:
        """Получение истории алертов"""
        return await self.db.get_alert_history(limit)
    
    async def get_module_status(self) -> Dict:
        """Получение статуса всех модулей"""
        return await self.db.get_module_status()

async def main():
    """Главная функция запуска бота"""
    bot = TeBiumAlertBot()
    
    # Определяем режим запуска
    if len(sys.argv) > 1 and sys.argv[1] == "webhook":
        webhook_url = os.getenv("WEBHOOK_URL", "https://your-domain.com")
        webhook_path = "/webhook"
        await bot.start_webhook(webhook_url, webhook_path)
    else:
        await bot.start_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
