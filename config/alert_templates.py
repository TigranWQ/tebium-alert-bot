"""
Шаблоны сообщений для алертов
"""

from typing import Dict, Any
from datetime import datetime

class AlertTemplates:
    """Шаблоны форматирования алертов"""
    
    # Эмодзи для разных типов алертов
    EMOJI_MAP = {
        "info": "ℹ️",
        "warning": "⚠️", 
        "error": "❌",
        "critical": "🚨",
        "success": "✅",
        "system": "🔧",
        "security": "🔒",
        "performance": "📊",
        "database": "🗄️",
        "api": "🌐",
        "bot": "🤖"
    }
    
    # Цвета для разных приоритетов (для будущего использования)
    COLOR_MAP = {
        "info": "#3498db",      # Синий
        "warning": "#f39c12",   # Оранжевый
        "error": "#e74c3c",     # Красный
        "critical": "#8e44ad"   # Фиолетовый
    }
    
    @staticmethod
    def format_alert(alert_data: Dict[str, Any]) -> str:
        """Форматирование алерта в сообщение"""
        emoji = AlertTemplates.EMOJI_MAP.get(alert_data.get("type", "info"), "ℹ️")
        priority_emoji = AlertTemplates.EMOJI_MAP.get(alert_data.get("priority", "info"), "ℹ️")
        
        # Заголовок
        title = f"{priority_emoji} **{alert_data.get('type', 'Alert').upper()}**"
        
        # Модуль
        module = alert_data.get("module", "unknown")
        module_emoji = AlertTemplates.EMOJI_MAP.get(module.split("-")[0].lower(), "🔧")
        
        # Время
        timestamp = alert_data.get("timestamp", datetime.now().isoformat())
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime("%H:%M:%S")
            except:
                time_str = timestamp
        else:
            time_str = timestamp.strftime("%H:%M:%S")
        
        # Основное сообщение
        message = alert_data.get("message", "No message")
        
        # Дополнительные данные
        data = alert_data.get("data", {})
        data_str = ""
        if data:
            data_str = "\n\n**Детали:**\n"
            for key, value in data.items():
                data_str += f"• {key}: `{value}`\n"
        
        # Формируем итоговое сообщение
        formatted_message = f"""
{title}
{emoji} **Модуль:** {module_emoji} `{module}`
🕐 **Время:** `{time_str}`
📝 **Сообщение:** {message}{data_str}
        """.strip()
        
        return formatted_message
    
    @staticmethod
    def format_system_status(status_data: Dict[str, Any]) -> str:
        """Форматирование статуса системы"""
        emoji = "🟢" if status_data.get("healthy", False) else "🔴"
        
        message = f"""
{emoji} **Статус системы**
🕐 **Время:** `{datetime.now().strftime('%H:%M:%S')}`
📊 **Модули:** {status_data.get('modules_online', 0)}/{status_data.get('total_modules', 0)}
💾 **Память:** {status_data.get('memory_usage', 'N/A')}
⚡ **CPU:** {status_data.get('cpu_usage', 'N/A')}
        """.strip()
        
        return message
    
    @staticmethod
    def format_module_alert(module: str, status: str, details: str = "") -> str:
        """Форматирование алерта модуля"""
        emoji = "✅" if status == "online" else "❌"
        
        message = f"""
{emoji} **Модуль:** `{module}`
📊 **Статус:** `{status.upper()}`
📝 **Детали:** {details}
🕐 **Время:** `{datetime.now().strftime('%H:%M:%S')}`
        """.strip()
        
        return message
    
    @staticmethod
    def format_error_alert(error_type: str, module: str, error_message: str, 
                          stack_trace: str = "") -> str:
        """Форматирование алерта об ошибке"""
        emoji = AlertTemplates.EMOJI_MAP.get("error", "❌")
        
        message = f"""
{emoji} **ОШИБКА МОДУЛЯ**
🔧 **Модуль:** `{module}`
⚠️ **Тип:** `{error_type}`
📝 **Сообщение:** `{error_message}`
🕐 **Время:** `{datetime.now().strftime('%H:%M:%S')}`
        """.strip()
        
        if stack_trace:
            message += f"\n\n**Stack Trace:**\n```\n{stack_trace[:500]}...\n```"
        
        return message
    
    @staticmethod
    def format_performance_alert(metric: str, value: float, threshold: float, 
                               module: str) -> str:
        """Форматирование алерта производительности"""
        emoji = "📊"
        
        message = f"""
{emoji} **ПРОИЗВОДИТЕЛЬНОСТЬ**
🔧 **Модуль:** `{module}`
📈 **Метрика:** `{metric}`
📊 **Значение:** `{value}`
⚠️ **Порог:** `{threshold}`
🕐 **Время:** `{datetime.now().strftime('%H:%M:%S')}`
        """.strip()
        
        return message
