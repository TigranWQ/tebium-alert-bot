"""
Менеджер алертов для TeBium Alert Bot
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import aiohttp
import json

from config.alert_templates import AlertTemplates

logger = logging.getLogger('TeBiumAlertBot')

class AlertManager:
    """Менеджер для обработки и отправки алертов"""
    
    def __init__(self, bot, database_manager):
        self.bot = bot
        self.db = database_manager
        self.alert_queue = asyncio.Queue()
        self.sent_alerts = {}  # Кэш для предотвращения дублирования
        self.rate_limits = {}  # Ограничения по частоте отправки
        
    async def process_alert(self, alert_data: Dict[str, Any]):
        """Обработка входящего алерта"""
        try:
            # Валидация данных алерта
            if not self._validate_alert_data(alert_data):
                logger.warning("⚠️ Некорректные данные алерта")
                return
            
            # Проверка cooldown
            module = alert_data.get('module', 'unknown')
            alert_type = alert_data.get('type', 'info')
            
            if not await self.db.get_alert_cooldown(module, alert_type):
                logger.info(f"⏳ Алерт от {module} заблокирован cooldown")
                return
            
            # Проверка rate limit
            if self._is_rate_limited(module, alert_type):
                logger.info(f"🚫 Алерт от {module} заблокирован rate limit")
                return
            
            # Сохранение в базу данных
            alert_id = await self.db.save_alert(alert_data)
            
            # Добавление в очередь отправки
            await self.alert_queue.put({
                'alert_id': alert_id,
                'alert_data': alert_data
            })
            
            # Обновление cooldown
            await self.db.update_alert_cooldown(module)
            
            # Обновление rate limit
            self._update_rate_limit(module, alert_type)
            
            logger.info(f"📨 Алерт {alert_id} добавлен в очередь")
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки алерта: {e}")
    
    async def start_alert_processor(self):
        """Запуск обработчика алертов"""
        logger.info("🚀 Запуск обработчика алертов")
        
        while True:
            try:
                # Получение алерта из очереди
                item = await self.alert_queue.get()
                alert_id = item['alert_id']
                alert_data = item['alert_data']
                
                # Отправка алерта
                await self._send_alert(alert_id, alert_data)
                
                # Отметка как обработанного
                self.alert_queue.task_done()
                
            except Exception as e:
                logger.error(f"❌ Ошибка в обработчике алертов: {e}")
                await asyncio.sleep(5)  # Пауза при ошибке
    
    async def _send_alert(self, alert_id: str, alert_data: Dict[str, Any]):
        """Отправка алерта в Telegram"""
        try:
            # Форматирование сообщения
            message_text = AlertTemplates.format_alert(alert_data)
            
            # Получение списка чатов для отправки
            chat_ids = await self.db.get_subscribed_chats(
                alert_type=alert_data.get('type'),
                module=alert_data.get('module')
            )
            
            if not chat_ids:
                logger.warning("⚠️ Нет подписчиков для алерта")
                return
            
            # Отправка в каждый чат
            for chat_id in chat_ids:
                try:
                    # Создание клавиатуры с кнопками
                    keyboard = self._create_alert_keyboard(alert_id, alert_data)
                    
                    # Отправка сообщения
                    message = await self.bot.send_message(
                        chat_id=chat_id,
                        text=message_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                    
                    # Отметка как отправленного
                    await self.db.mark_alert_sent(alert_id, chat_id, message.message_id)
                    
                    logger.info(f"✅ Алерт {alert_id} отправлен в чат {chat_id}")
                    
                except Exception as e:
                    logger.error(f"❌ Ошибка отправки в чат {chat_id}: {e}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки алерта {alert_id}: {e}")
    
    def _create_alert_keyboard(self, alert_id: str, alert_data: Dict[str, Any]) -> Optional[Any]:
        """Создание клавиатуры для алерта"""
        try:
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Подтвердить",
                        callback_data=f"confirm_{alert_id}"
                    ),
                    InlineKeyboardButton(
                        text="⏰ Отложить",
                        callback_data=f"delay_{alert_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📊 Детали",
                        callback_data=f"details_{alert_id}"
                    ),
                    InlineKeyboardButton(
                        text="🔕 Отключить",
                        callback_data=f"mute_{alert_id}"
                    )
                ]
            ])
            
            return keyboard
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания клавиатуры: {e}")
            return None
    
    def _validate_alert_data(self, alert_data: Dict[str, Any]) -> bool:
        """Валидация данных алерта"""
        required_fields = ['type', 'message', 'module']
        
        for field in required_fields:
            if field not in alert_data or not alert_data[field]:
                logger.warning(f"⚠️ Отсутствует обязательное поле: {field}")
                return False
        
        return True
    
    def _is_rate_limited(self, module: str, alert_type: str) -> bool:
        """Проверка rate limit для модуля"""
        key = f"{module}_{alert_type}"
        now = datetime.now()
        
        if key not in self.rate_limits:
            self.rate_limits[key] = []
        
        # Очистка старых записей (старше часа)
        hour_ago = now - timedelta(hours=1)
        self.rate_limits[key] = [
            timestamp for timestamp in self.rate_limits[key] 
            if timestamp > hour_ago
        ]
        
        # Проверка лимита (максимум 100 алертов в час)
        if len(self.rate_limits[key]) >= 100:
            return True
        
        return False
    
    def _update_rate_limit(self, module: str, alert_type: str):
        """Обновление rate limit"""
        key = f"{module}_{alert_type}"
        if key not in self.rate_limits:
            self.rate_limits[key] = []
        
        self.rate_limits[key].append(datetime.now())
    
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
        
        await self.process_alert(alert_data)
    
    async def check_module_health(self, module_name: str, health_url: str):
        """Проверка здоровья модуля"""
        try:
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                
                async with session.get(health_url, timeout=10) as response:
                    response_time = (datetime.now() - start_time).total_seconds()
                    
                    if response.status == 200:
                        status = "online"
                        await self.db.update_module_status(
                            module_name, status, response_time
                        )
                        logger.info(f"✅ Модуль {module_name} онлайн")
                    else:
                        status = "error"
                        await self.db.update_module_status(
                            module_name, status, response_time, 
                            f"HTTP {response.status}"
                        )
                        logger.warning(f"⚠️ Модуль {module_name} недоступен: HTTP {response.status}")
                        
        except asyncio.TimeoutError:
            await self.db.update_module_status(
                module_name, "timeout", None, "Timeout"
            )
            logger.error(f"⏰ Таймаут проверки модуля {module_name}")
            
        except Exception as e:
            await self.db.update_module_status(
                module_name, "error", None, str(e)
            )
            logger.error(f"❌ Ошибка проверки модуля {module_name}: {e}")
    
    async def get_alert_statistics(self) -> Dict[str, Any]:
        """Получение статистики алертов"""
        try:
            history = await self.db.get_alert_history(1000)  # Последние 1000 алертов
            
            stats = {
                'total_alerts': len(history),
                'by_type': {},
                'by_module': {},
                'by_priority': {},
                'recent_alerts': len([a for a in history if 
                                    datetime.fromisoformat(a['timestamp']) > 
                                    datetime.now() - timedelta(hours=1)])
            }
            
            for alert in history:
                # Статистика по типам
                alert_type = alert['type']
                stats['by_type'][alert_type] = stats['by_type'].get(alert_type, 0) + 1
                
                # Статистика по модулям
                module = alert['module']
                stats['by_module'][module] = stats['by_module'].get(module, 0) + 1
                
                # Статистика по приоритетам
                priority = alert['priority']
                stats['by_priority'][priority] = stats['by_priority'].get(priority, 0) + 1
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статистики: {e}")
            return {}
