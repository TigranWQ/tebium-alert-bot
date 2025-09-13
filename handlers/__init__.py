"""
Обработчики команд для TeBium Alert Bot
"""

from .admin_handlers import register_admin_handlers
from .alert_handlers import register_alert_handlers
from .system_handlers import register_system_handlers

def register_handlers(dp, alert_manager):
    """Регистрация всех обработчиков"""
    register_admin_handlers(dp, alert_manager)
    register_alert_handlers(dp, alert_manager)
    register_system_handlers(dp, alert_manager)