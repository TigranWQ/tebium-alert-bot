"""
Системные обработчики для TeBium Alert Bot
"""

import logging
from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from config.alert_templates import AlertTemplates

logger = logging.getLogger('TeBiumAlertBot')

def register_system_handlers(dp: Dispatcher, alert_manager):
    """Регистрация системных обработчиков"""
    
    @dp.message(CommandStart())
    async def start_command(message: Message):
        """Обработчик команды /start"""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
                InlineKeyboardButton(text="🔧 Статус модулей", callback_data="modules")
            ],
            [
                InlineKeyboardButton(text="📋 История алертов", callback_data="history"),
                InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
            ]
        ])
        
        await message.answer(
            "🚨 **TeBium Alert Bot**\n\n"
            "Добро пожаловать в систему мониторинга и алертов TeBium!\n\n"
            "Этот бот отслеживает состояние всех модулей системы и отправляет уведомления о проблемах.\n\n"
            "Выберите действие:",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    
    @dp.message(Command("help"))
    async def help_command(message: Message):
        """Обработчик команды /help"""
        help_text = """
🚨 **TeBium Alert Bot - Справка**

**Основные команды:**
• `/start` - Главное меню
• `/help` - Эта справка
• `/status` - Статус системы
• `/stats` - Статистика алертов
• `/admin` - Панель администратора

**Что делает бот:**
• 🔍 Мониторит состояние всех модулей TeBium
• 📨 Отправляет уведомления о проблемах
• 📊 Ведет статистику алертов
• ⚙️ Позволяет управлять настройками

**Типы алертов:**
• ℹ️ **info** - Информационные сообщения
• ⚠️ **warning** - Предупреждения
• ❌ **error** - Ошибки
• 🚨 **critical** - Критические проблемы

**Мониторируемые модули:**
• TeBium-Analytics-Server
• Telegram-Bot-Tebium
• TeBium-Alert-Bot

Для получения помощи обратитесь к администратору.
        """
        
        await message.answer(help_text, parse_mode='Markdown')
    
    @dp.message(Command("status"))
    async def status_command(message: Message, alert_manager):
        """Обработчик команды /status"""
        try:
            status_data = await alert_manager.db.get_module_status()
            
            message_text = AlertTemplates.format_system_status(status_data)
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_status"),
                    InlineKeyboardButton(text="📊 Детали", callback_data="status_details")
                ]
            ])
            
            await message.answer(message_text, reply_markup=keyboard, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статуса: {e}")
            await message.answer("❌ Ошибка получения статуса системы")
    
    @dp.message(Command("stats"))
    async def stats_command(message: Message, alert_manager):
        """Обработчик команды /stats"""
        try:
            stats = await alert_manager.get_alert_statistics()
            
            message_text = f"""
📊 **Статистика алертов**

📈 **Общее количество:** {stats.get('total_alerts', 0)}
🕐 **За последний час:** {stats.get('recent_alerts', 0)}

📋 **По типам:**
"""
            for alert_type, count in stats.get('by_type', {}).items():
                emoji = AlertTemplates.EMOJI_MAP.get(alert_type, 'ℹ️')
                message_text += f"{emoji} {alert_type}: {count}\n"
            
            message_text += "\n🔧 **По модулям:**\n"
            for module, count in stats.get('by_module', {}).items():
                message_text += f"🔧 {module}: {count}\n"
            
            message_text += "\n⚠️ **По приоритетам:**\n"
            for priority, count in stats.get('by_priority', {}).items():
                emoji = AlertTemplates.EMOJI_MAP.get(priority, 'ℹ️')
                message_text += f"{emoji} {priority}: {count}\n"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_stats"),
                    InlineKeyboardButton(text="📋 История", callback_data="history")
                ]
            ])
            
            await message.answer(message_text, reply_markup=keyboard, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статистики: {e}")
            await message.answer("❌ Ошибка получения статистики")
    
    @dp.message(Command("ping"))
    async def ping_command(message: Message):
        """Обработчик команды /ping"""
        start_time = datetime.now()
        
        # Имитация обработки
        await asyncio.sleep(0.1)
        
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        
        await message.answer(
            f"🏓 **Pong!**\n"
            f"⏱️ Время ответа: `{response_time:.2f}ms`\n"
            f"🕐 Время: `{datetime.now().strftime('%H:%M:%S')}`",
            parse_mode='Markdown'
        )
    
    @dp.message(Command("test"))
    async def test_command(message: Message, alert_manager):
        """Обработчик команды /test - отправка тестового алерта"""
        try:
            await alert_manager.send_system_alert(
                alert_type="test",
                message="Это тестовое сообщение от TeBium Alert Bot",
                priority="info",
                module="TeBium-Alert-Bot",
                data={"test": True, "timestamp": datetime.now().isoformat()}
            )
            
            await message.answer("✅ Тестовый алерт отправлен!")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки тестового алерта: {e}")
            await message.answer("❌ Ошибка отправки тестового алерта")
    
    @dp.message()
    async def handle_unknown_message(message: Message):
        """Обработчик неизвестных сообщений"""
        await message.answer(
            "❓ Неизвестная команда.\n\n"
            "Используйте /help для получения справки или /start для главного меню."
        )
