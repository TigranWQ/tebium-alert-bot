"""
Тесты для TeBium Alert Bot
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from config.settings import Settings
from utils.database import DatabaseManager
from utils.alert_manager import AlertManager
from config.alert_templates import AlertTemplates

class TestAlertTemplates:
    """Тесты для шаблонов алертов"""
    
    def test_format_alert(self):
        """Тест форматирования алерта"""
        alert_data = {
            "type": "error",
            "priority": "critical",
            "module": "test-module",
            "message": "Test error message",
            "timestamp": datetime.now().isoformat(),
            "data": {"test": True}
        }
        
        formatted = AlertTemplates.format_alert(alert_data)
        
        assert "ERROR" in formatted
        assert "test-module" in formatted
        assert "Test error message" in formatted
        assert "🚨" in formatted  # Эмодзи для critical
    
    def test_format_system_status(self):
        """Тест форматирования статуса системы"""
        status_data = {
            "healthy": True,
            "modules_online": 3,
            "total_modules": 3,
            "memory_usage": "50%",
            "cpu_usage": "25%"
        }
        
        formatted = AlertTemplates.format_system_status(status_data)
        
        assert "Статус системы" in formatted
        assert "3/3" in formatted
        assert "50%" in formatted
        assert "25%" in formatted

class TestDatabaseManager:
    """Тесты для менеджера базы данных"""
    
    @pytest.fixture
    def db_manager(self):
        """Фикстура для менеджера БД"""
        return DatabaseManager("sqlite:///:memory:")
    
    @pytest.mark.asyncio
    async def test_init_database(self, db_manager):
        """Тест инициализации базы данных"""
        await db_manager.init_database()
        # Если не выброшено исключение, значит инициализация прошла успешно
        assert True
    
    @pytest.mark.asyncio
    async def test_save_alert(self, db_manager):
        """Тест сохранения алерта"""
        await db_manager.init_database()
        
        alert_data = {
            "type": "test",
            "priority": "info",
            "module": "test-module",
            "message": "Test message",
            "timestamp": datetime.now().isoformat(),
            "data": {}
        }
        
        alert_id = await db_manager.save_alert(alert_data)
        assert alert_id is not None
        assert "test-module" in alert_id

class TestAlertManager:
    """Тесты для менеджера алертов"""
    
    @pytest.fixture
    def mock_bot(self):
        """Мок бота"""
        bot = Mock()
        bot.send_message = AsyncMock()
        return bot
    
    @pytest.fixture
    def mock_db(self):
        """Мок базы данных"""
        db = Mock()
        db.save_alert = AsyncMock(return_value="test-alert-id")
        db.get_alert_cooldown = AsyncMock(return_value=True)
        db.update_alert_cooldown = AsyncMock()
        db.get_subscribed_chats = AsyncMock(return_value=["123456789"])
        db.mark_alert_sent = AsyncMock()
        return db
    
    @pytest.fixture
    def alert_manager(self, mock_bot, mock_db):
        """Фикстура для менеджера алертов"""
        return AlertManager(mock_bot, mock_db)
    
    @pytest.mark.asyncio
    async def test_process_alert(self, alert_manager):
        """Тест обработки алерта"""
        alert_data = {
            "type": "test",
            "priority": "info",
            "module": "test-module",
            "message": "Test message",
            "timestamp": datetime.now().isoformat(),
            "data": {}
        }
        
        await alert_manager.process_alert(alert_data)
        
        # Проверяем, что алерт был сохранен
        alert_manager.db.save_alert.assert_called_once()
        alert_manager.db.update_alert_cooldown.assert_called_once()
    
    def test_validate_alert_data(self, alert_manager):
        """Тест валидации данных алерта"""
        # Валидные данные
        valid_data = {
            "type": "test",
            "message": "Test message",
            "module": "test-module"
        }
        assert alert_manager._validate_alert_data(valid_data) == True
        
        # Невалидные данные (отсутствует type)
        invalid_data = {
            "message": "Test message",
            "module": "test-module"
        }
        assert alert_manager._validate_alert_data(invalid_data) == False
    
    def test_rate_limiting(self, alert_manager):
        """Тест rate limiting"""
        module = "test-module"
        alert_type = "test"
        
        # Первый алерт должен пройти
        assert not alert_manager._is_rate_limited(module, alert_type)
        
        # Обновляем rate limit
        alert_manager._update_rate_limit(module, alert_type)
        
        # Второй алерт тоже должен пройти (лимит 100 в час)
        assert not alert_manager._is_rate_limited(module, alert_type)

@pytest.mark.asyncio
async def test_integration():
    """Интеграционный тест"""
    # Создаем реальные объекты для интеграционного теста
    settings = Settings()
    db = DatabaseManager("sqlite:///:memory:")
    
    await db.init_database()
    
    # Создаем мок бота
    mock_bot = Mock()
    mock_bot.send_message = AsyncMock()
    
    alert_manager = AlertManager(mock_bot, db)
    
    # Отправляем тестовый алерт
    await alert_manager.send_system_alert(
        alert_type="test",
        message="Integration test message",
        priority="info",
        module="test-module"
    )
    
    # Проверяем, что алерт был сохранен в БД
    history = await db.get_alert_history(10)
    assert len(history) == 1
    assert history[0]["type"] == "test"
    assert history[0]["message"] == "Integration test message"

if __name__ == "__main__":
    pytest.main([__file__])
