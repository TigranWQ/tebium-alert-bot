"""
Настройки TeBium Alert Bot
"""

import os
from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Настройки бота"""
    
    # Telegram Bot настройки
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "your-secret-key")
    WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", "8082"))
    
    # База данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///data/alerts.db")
    
    # Настройки алертов
    ALERT_CHAT_ID: str = os.getenv("ALERT_CHAT_ID", "")
    ENABLE_ALERTS: bool = os.getenv("ENABLE_ALERTS", "true").lower() == "true"
    
    # Приоритеты алертов
    PRIORITY_LEVELS: List[str] = ["info", "warning", "error", "critical"]
    
    # Настройки модулей для мониторинга
    MONITORED_MODULES: List[str] = [
        "TeBium-Analytics-Server",
        "Telegram-Bot-Tebium", 
        "TeBium-Alert-Bot"
    ]
    
    # Настройки уведомлений
    ALERT_COOLDOWN: int = int(os.getenv("ALERT_COOLDOWN", "60"))  # секунды
    MAX_ALERTS_PER_HOUR: int = int(os.getenv("MAX_ALERTS_PER_HOUR", "100"))
    
    # Настройки форматирования
    ENABLE_EMOJI: bool = os.getenv("ENABLE_EMOJI", "true").lower() == "true"
    ENABLE_MARKDOWN: bool = os.getenv("ENABLE_MARKDOWN", "true").lower() == "true"
    
    # Настройки логирования
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/alert_bot.log")
    
    # API настройки для интеграции с другими модулями
    ANALYTICS_SERVER_URL: str = os.getenv("ANALYTICS_SERVER_URL", "http://localhost:8081")
    MAIN_BOT_URL: str = os.getenv("MAIN_BOT_URL", "http://localhost:8080")
    
    # Настройки retry
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "5"))
    
    class Config:
        env_file = "config.env"
        case_sensitive = True
