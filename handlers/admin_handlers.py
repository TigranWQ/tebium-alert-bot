"""
Административные обработчики для TeBium Alert Bot
"""

import logging
from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config.alert_templates import AlertTemplates

logger = logging.getLogger('TeBiumAlertBot')

class AdminStates(StatesGroup):
    waiting_for_chat_id = State()
    waiting_for_alert_message = State()

def register_admin_handlers(dp: Dispatcher, alert_manager):
    """Регистрация административных обработчиков"""
    
    @dp.message(Command("admin"))
    async def admin_panel(message: Message):
        """Панель администратора"""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
                InlineKeyboardButton(text="🔧 Модули", callback_data="admin_modules")
            ],
            [
                InlineKeyboardButton(text="📨 Отправить алерт", callback_data="admin_send_alert"),
                InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_settings")
            ],
            [
                InlineKeyboardButton(text="📋 История", callback_data="admin_history"),
                InlineKeyboardButton(text="🔄 Проверить модули", callback_data="admin_check_modules")
            ]
        ])
        
        await message.answer(
            "🔧 **Панель администратора**\n\n"
            "Выберите действие:",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    
    @dp.callback_query(F.data == "admin_stats")
    async def show_statistics(callback: CallbackQuery, alert_manager):
        """Показать статистику алертов"""
        try:
            stats = await alert_manager.get_alert_statistics()
            
            message = f"""
📊 **Статистика алертов**

📈 **Общее количество:** {stats.get('total_alerts', 0)}
🕐 **За последний час:** {stats.get('recent_alerts', 0)}

📋 **По типам:**
"""
            for alert_type, count in stats.get('by_type', {}).items():
                message += f"• {alert_type}: {count}\n"
            
            message += "\n🔧 **По модулям:**\n"
            for module, count in stats.get('by_module', {}).items():
                message += f"• {module}: {count}\n"
            
            message += "\n⚠️ **По приоритетам:**\n"
            for priority, count in stats.get('by_priority', {}).items():
                message += f"• {priority}: {count}\n"
            
            await callback.message.edit_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статистики: {e}")
            await callback.answer("❌ Ошибка получения статистики")
    
    @dp.callback_query(F.data == "admin_modules")
    async def show_modules_status(callback: CallbackQuery, alert_manager):
        """Показать статус модулей"""
        try:
            status_data = await alert_manager.db.get_module_status()
            
            message = "🔧 **Статус модулей**\n\n"
            
            for module_name, module_info in status_data.get('modules', {}).items():
                status_emoji = "✅" if module_info['status'] == 'online' else "❌"
                response_time = module_info.get('response_time', 'N/A')
                
                message += f"{status_emoji} **{module_name}**\n"
                message += f"   Статус: `{module_info['status']}`\n"
                message += f"   Время ответа: `{response_time}ms`\n"
                message += f"   Последняя проверка: `{module_info['last_check']}`\n\n"
            
            await callback.message.edit_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статуса модулей: {e}")
            await callback.answer("❌ Ошибка получения статуса модулей")
    
    @dp.callback_query(F.data == "admin_send_alert")
    async def start_send_alert(callback: CallbackQuery, state: FSMContext):
        """Начать процесс отправки алерта"""
        await state.set_state(AdminStates.waiting_for_alert_message)
        await callback.message.edit_text(
            "📨 **Отправка алерта**\n\n"
            "Отправьте сообщение в формате:\n"
            "`тип|приоритет|модуль|сообщение`\n\n"
            "Пример: `error|critical|system|Сервер недоступен`",
            parse_mode='Markdown'
        )
    
    @dp.message(AdminStates.waiting_for_alert_message)
    async def process_alert_message(message: Message, state: FSMContext, alert_manager):
        """Обработка сообщения с алертом"""
        try:
            parts = message.text.split('|', 3)
            if len(parts) != 4:
                await message.answer(
                    "❌ Неверный формат. Используйте:\n"
                    "`тип|приоритет|модуль|сообщение`"
                )
                return
            
            alert_type, priority, module, alert_message = parts
            
            await alert_manager.send_system_alert(
                alert_type=alert_type.strip(),
                message=alert_message.strip(),
                priority=priority.strip(),
                module=module.strip()
            )
            
            await message.answer("✅ Алерт отправлен!")
            await state.clear()
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки алерта: {e}")
            await message.answer("❌ Ошибка отправки алерта")
            await state.clear()
    
    @dp.callback_query(F.data == "admin_check_modules")
    async def check_modules_health(callback: CallbackQuery, alert_manager):
        """Проверка здоровья модулей"""
        try:
            await callback.answer("🔄 Проверяю модули...")
            
            # Список модулей для проверки
            modules_to_check = [
                ("TeBium-Analytics-Server", "http://localhost:8081/health"),
                ("Telegram-Bot-Tebium", "http://localhost:8080/health"),
            ]
            
            for module_name, health_url in modules_to_check:
                await alert_manager.check_module_health(module_name, health_url)
            
            await callback.message.edit_text("✅ Проверка модулей завершена")
            
        except Exception as e:
            logger.error(f"❌ Ошибка проверки модулей: {e}")
            await callback.answer("❌ Ошибка проверки модулей")
    
    @dp.callback_query(F.data == "admin_history")
    async def show_alert_history(callback: CallbackQuery, alert_manager):
        """Показать историю алертов"""
        try:
            history = await alert_manager.db.get_alert_history(10)
            
            if not history:
                await callback.message.edit_text("📋 История алертов пуста")
                return
            
            message = "📋 **Последние алерты**\n\n"
            
            for alert in history[:10]:
                timestamp = alert['timestamp'][:19]  # Обрезаем до секунд
                emoji = AlertTemplates.EMOJI_MAP.get(alert['priority'], 'ℹ️')
                
                message += f"{emoji} **{alert['type']}** - {alert['module']}\n"
                message += f"   {alert['message'][:50]}...\n"
                message += f"   `{timestamp}`\n\n"
            
            await callback.message.edit_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения истории: {e}")
            await callback.answer("❌ Ошибка получения истории")
    
    @dp.callback_query(F.data == "admin_settings")
    async def show_settings(callback: CallbackQuery):
        """Показать настройки"""
        message = """
⚙️ **Настройки бота**

🔧 **Мониторинг модулей:**
• TeBium-Analytics-Server: ✅
• Telegram-Bot-Tebium: ✅
• TeBium-Alert-Bot: ✅

📊 **Лимиты:**
• Максимум алертов в час: 100
• Cooldown между алертами: 60 сек
• Таймаут проверки модулей: 10 сек

🔔 **Уведомления:**
• Эмодзи: ✅
• Markdown: ✅
• Кнопки действий: ✅
        """
        
        await callback.message.edit_text(message, parse_mode='Markdown')
