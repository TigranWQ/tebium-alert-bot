"""
Управление базой данных для TeBium Alert Bot
"""

import sqlite3
import asyncio
import aiosqlite
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger('TeBiumAlertBot')

class DatabaseManager:
    """Менеджер базы данных для алертов"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.db_path = database_url.replace("sqlite:///", "")
        
    async def init_database(self):
        """Инициализация базы данных"""
        try:
            # Создаем папку для базы данных
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            
            async with aiosqlite.connect(self.db_path) as db:
                # Таблица алертов
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        alert_id TEXT UNIQUE NOT NULL,
                        type TEXT NOT NULL,
                        priority TEXT NOT NULL,
                        module TEXT NOT NULL,
                        message TEXT NOT NULL,
                        data TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        sent BOOLEAN DEFAULT FALSE,
                        chat_id TEXT,
                        message_id INTEGER
                    )
                """)
                
                # Таблица настроек модулей
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS module_settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        module_name TEXT UNIQUE NOT NULL,
                        enabled BOOLEAN DEFAULT TRUE,
                        alert_types TEXT,
                        cooldown INTEGER DEFAULT 60,
                        last_alert DATETIME,
                        settings TEXT
                    )
                """)
                
                # Таблица истории статусов
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS module_status (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        module_name TEXT NOT NULL,
                        status TEXT NOT NULL,
                        last_check DATETIME DEFAULT CURRENT_TIMESTAMP,
                        details TEXT,
                        response_time REAL
                    )
                """)
                
                # Таблица подписок на алерты
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS alert_subscriptions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id TEXT NOT NULL,
                        alert_types TEXT,
                        modules TEXT,
                        priority_levels TEXT,
                        enabled BOOLEAN DEFAULT TRUE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                await db.commit()
                logger.info("✅ База данных инициализирована")
                
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации БД: {e}")
            raise
    
    async def save_alert(self, alert_data: Dict[str, Any]) -> str:
        """Сохранение алерта в базу данных"""
        try:
            alert_id = f"{alert_data['module']}_{int(datetime.now().timestamp())}"
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO alerts 
                    (alert_id, type, priority, module, message, data, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert_id,
                    alert_data.get('type', 'info'),
                    alert_data.get('priority', 'info'),
                    alert_data.get('module', 'unknown'),
                    alert_data.get('message', ''),
                    json.dumps(alert_data.get('data', {})),
                    alert_data.get('timestamp', datetime.now().isoformat())
                ))
                await db.commit()
                
            logger.info(f"💾 Алерт сохранен: {alert_id}")
            return alert_id
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения алерта: {e}")
            raise
    
    async def mark_alert_sent(self, alert_id: str, chat_id: str, message_id: int):
        """Отметка алерта как отправленного"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    UPDATE alerts 
                    SET sent = TRUE, chat_id = ?, message_id = ?
                    WHERE alert_id = ?
                """, (chat_id, message_id, alert_id))
                await db.commit()
                
        except Exception as e:
            logger.error(f"❌ Ошибка обновления статуса алерта: {e}")
    
    async def get_alert_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Получение истории алертов"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT * FROM alerts 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
                rows = await cursor.fetchall()
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения истории: {e}")
            return []
    
    async def get_module_status(self) -> Dict[str, Any]:
        """Получение статуса всех модулей"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("""
                    SELECT module_name, status, last_check, response_time
                    FROM module_status 
                    ORDER BY last_check DESC
                """)
                rows = await cursor.fetchall()
                
                modules = {}
                for row in rows:
                    modules[row['module_name']] = {
                        'status': row['status'],
                        'last_check': row['last_check'],
                        'response_time': row['response_time']
                    }
                
                return {
                    'modules': modules,
                    'total_modules': len(modules),
                    'modules_online': len([m for m in modules.values() if m['status'] == 'online']),
                    'last_update': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения статуса модулей: {e}")
            return {'modules': {}, 'total_modules': 0, 'modules_online': 0}
    
    async def update_module_status(self, module_name: str, status: str, 
                                 response_time: Optional[float] = None, 
                                 details: Optional[str] = None):
        """Обновление статуса модуля"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO module_status 
                    (module_name, status, last_check, response_time, details)
                    VALUES (?, ?, ?, ?, ?)
                """, (module_name, status, datetime.now().isoformat(), 
                     response_time, details))
                await db.commit()
                
        except Exception as e:
            logger.error(f"❌ Ошибка обновления статуса модуля: {e}")
    
    async def get_alert_cooldown(self, module: str, alert_type: str) -> bool:
        """Проверка cooldown для алертов"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("""
                    SELECT last_alert, cooldown FROM module_settings 
                    WHERE module_name = ? AND enabled = TRUE
                """, (module,))
                row = await cursor.fetchone()
                
                if not row:
                    return True  # Нет настроек - можно отправлять
                
                last_alert = datetime.fromisoformat(row[0]) if row[0] else None
                cooldown = row[1] or 60
                
                if not last_alert:
                    return True
                
                time_diff = (datetime.now() - last_alert).total_seconds()
                return time_diff >= cooldown
                
        except Exception as e:
            logger.error(f"❌ Ошибка проверки cooldown: {e}")
            return True
    
    async def update_alert_cooldown(self, module: str):
        """Обновление времени последнего алерта"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    UPDATE module_settings 
                    SET last_alert = ?
                    WHERE module_name = ?
                """, (datetime.now().isoformat(), module))
                await db.commit()
                
        except Exception as e:
            logger.error(f"❌ Ошибка обновления cooldown: {e}")
    
    async def get_subscribed_chats(self, alert_type: str = None, 
                                 module: str = None) -> List[str]:
        """Получение списка чатов для отправки алертов"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                query = "SELECT chat_id FROM alert_subscriptions WHERE enabled = TRUE"
                params = []
                
                if alert_type:
                    query += " AND (alert_types IS NULL OR alert_types LIKE ?)"
                    params.append(f"%{alert_type}%")
                
                if module:
                    query += " AND (modules IS NULL OR modules LIKE ?)"
                    params.append(f"%{module}%")
                
                cursor = await db.execute(query, params)
                rows = await cursor.fetchall()
                
                return [row[0] for row in rows]
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения подписок: {e}")
            return []
