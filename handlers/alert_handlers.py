"""
Обработчики алертов для TeBium Alert Bot
"""

import logging
from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

logger = logging.getLogger('TeBiumAlertBot')

def register_alert_handlers(dp: Dispatcher, alert_manager):
    """Регистрация обработчиков алертов"""
    
    @dp.callback_query(F.data.startswith("confirm_"))
    async def confirm_alert(callback: CallbackQuery, alert_manager):
        """Подтверждение алерта"""
        alert_id = callback.data.replace("confirm_", "")
        
        try:
            # Здесь можно добавить логику подтверждения алерта
            # Например, обновление статуса в базе данных
            
            await callback.answer("✅ Алерт подтвержден")
            
            # Обновляем сообщение
            await callback.message.edit_text(
                callback.message.text + "\n\n✅ **Подтверждено**",
                reply_markup=callback.message.reply_markup
            )
            
        except Exception as e:
            logger.error(f"❌ Ошибка подтверждения алерта: {e}")
            await callback.answer("❌ Ошибка подтверждения")
    
    @dp.callback_query(F.data.startswith("delay_"))
    async def delay_alert(callback: CallbackQuery, alert_manager):
        """Отложение алерта"""
        alert_id = callback.data.replace("delay_", "")
        
        try:
            # Создаем клавиатуру для выбора времени отложения
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="⏰ 5 мин", callback_data=f"delay_5_{alert_id}"),
                    InlineKeyboardButton(text="⏰ 15 мин", callback_data=f"delay_15_{alert_id}"),
                    InlineKeyboardButton(text="⏰ 30 мин", callback_data=f"delay_30_{alert_id}")
                ],
                [
                    InlineKeyboardButton(text="⏰ 1 час", callback_data=f"delay_60_{alert_id}"),
                    InlineKeyboardButton(text="⏰ 2 часа", callback_data=f"delay_120_{alert_id}"),
                    InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel_delay_{alert_id}")
                ]
            ])
            
            await callback.message.edit_text(
                callback.message.text + "\n\n⏰ **Выберите время отложения:**",
                reply_markup=keyboard
            )
            
        except Exception as e:
            logger.error(f"❌ Ошибка отложения алерта: {e}")
            await callback.answer("❌ Ошибка отложения")
    
    @dp.callback_query(F.data.startswith("delay_") and F.data.count("_") == 2)
    async def process_delay_alert(callback: CallbackQuery, alert_manager):
        """Обработка отложения алерта"""
        try:
            parts = callback.data.split("_")
            delay_minutes = int(parts[1])
            alert_id = parts[2]
            
            # Здесь можно добавить логику отложения алерта
            # Например, планирование повторной отправки через указанное время
            
            await callback.answer(f"⏰ Алерт отложен на {delay_minutes} минут")
            
            await callback.message.edit_text(
                callback.message.text + f"\n\n⏰ **Отложено на {delay_minutes} минут**",
                reply_markup=None
            )
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки отложения: {e}")
            await callback.answer("❌ Ошибка отложения")
    
    @dp.callback_query(F.data.startswith("details_"))
    async def show_alert_details(callback: CallbackQuery, alert_manager):
        """Показать детали алерта"""
        alert_id = callback.data.replace("details_", "")
        
        try:
            # Получаем детали алерта из базы данных
            history = await alert_manager.db.get_alert_history(1000)
            alert = next((a for a in history if a['alert_id'] == alert_id), None)
            
            if not alert:
                await callback.answer("❌ Алерт не найден")
                return
            
            details = f"""
📋 **Детали алерта**

🆔 **ID:** `{alert['alert_id']}`
📝 **Тип:** `{alert['type']}`
⚠️ **Приоритет:** `{alert['priority']}`
🔧 **Модуль:** `{alert['module']}`
📅 **Время:** `{alert['timestamp']}`
📤 **Отправлен:** {'✅' if alert['sent'] else '❌'}

📄 **Сообщение:**
{alert['message']}
            """
            
            if alert['data']:
                details += f"\n\n📊 **Дополнительные данные:**\n{alert['data']}"
            
            await callback.message.edit_text(details, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения деталей: {e}")
            await callback.answer("❌ Ошибка получения деталей")
    
    @dp.callback_query(F.data.startswith("mute_"))
    async def mute_alert(callback: CallbackQuery, alert_manager):
        """Отключение уведомлений для типа алерта"""
        alert_id = callback.data.replace("mute_", "")
        
        try:
            # Здесь можно добавить логику отключения уведомлений
            # Например, добавление в список игнорируемых типов алертов
            
            await callback.answer("🔕 Уведомления отключены для этого типа алертов")
            
            await callback.message.edit_text(
                callback.message.text + "\n\n🔕 **Уведомления отключены**",
                reply_markup=None
            )
            
        except Exception as e:
            logger.error(f"❌ Ошибка отключения уведомлений: {e}")
            await callback.answer("❌ Ошибка отключения")
    
    @dp.callback_query(F.data.startswith("cancel_delay_"))
    async def cancel_delay(callback: CallbackQuery):
        """Отмена отложения алерта"""
        await callback.answer("❌ Отложение отменено")
        
        # Возвращаем оригинальную клавиатуру
        original_text = callback.message.text.replace("\n\n⏰ **Выберите время отложения:**", "")
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_{callback.data.replace('cancel_delay_', '')}"),
                InlineKeyboardButton(text="⏰ Отложить", callback_data=f"delay_{callback.data.replace('cancel_delay_', '')}")
            ],
            [
                InlineKeyboardButton(text="📊 Детали", callback_data=f"details_{callback.data.replace('cancel_delay_', '')}"),
                InlineKeyboardButton(text="🔕 Отключить", callback_data=f"mute_{callback.data.replace('cancel_delay_', '')}")
            ]
        ])
        
        await callback.message.edit_text(original_text, reply_markup=keyboard)
