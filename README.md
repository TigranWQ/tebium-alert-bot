# 🚨 TeBium Alert Bot

Модуль для отправки системных уведомлений и алертов в Telegram для экосистемы TeBium.

## 🌐 Часть экосистемы TeBium

Этот модуль является частью модульной экосистемы TeBium:

- **[TeBium-Analytics-Server](https://github.com/TigranWQ/tebium-analytics-server)** - C++ сервер аналитики
- **[Telegram-Bot-Tebium](https://github.com/TigranWQ/telegram-bot-tebium)** - Основной Telegram бот
- **[TeBium-Alert-Bot](https://github.com/TigranWQ/tebium-alert-bot)** - Бот для алертов (текущий модуль)

Подробнее см. [ECOSYSTEM.md](ECOSYSTEM.md)

## 📋 Обзор

TeBium Alert Bot - это специализированный Telegram бот, который отвечает за мониторинг состояния всех модулей системы TeBium и отправку уведомлений о проблемах, ошибках и важных событиях.

## 🎯 Основные функции

### 🔍 Мониторинг модулей
- **Автоматическая проверка** состояния всех модулей TeBium
- **Health checks** для TeBium-Analytics-Server, Telegram-Bot-Tebium и других модулей
- **Отслеживание производительности** и времени ответа

### 📨 Система алертов
- **Мгновенные уведомления** о критических проблемах
- **Приоритизация алертов** (info, warning, error, critical)
- **Группировка по модулям** и типам событий
- **Rate limiting** для предотвращения спама

### 🎨 Форматирование сообщений
- **Эмодзи и цветовое кодирование** по приоритету
- **Markdown форматирование** для читаемости
- **Интерактивные кнопки** для быстрых действий
- **Детальная информация** об алертах

### ⚙️ Управление
- **Административная панель** для управления ботом
- **Статистика алертов** и производительности
- **История событий** с возможностью поиска
- **Настройка подписок** на типы алертов

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                TeBium Alert Bot                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────┐ │
│  │  Alert Manager  │  │  Database       │  │  Bot    │ │
│  │  - Processing   │  │  - SQLite       │  │  - AIO  │ │
│  │  - Rate Limit   │  │  - History      │  │  - Web  │ │
│  │  - Templates    │  │  - Settings     │  │  - API  │ │
│  └─────────────────┘  └─────────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/Webhook
                                ▼
┌─────────────────────────────────────────────────────────┐
│              Другие модули TeBium                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────┐ │
│  │ Analytics       │  │ Main Bot        │  │ Other   │ │
│  │ Server          │  │                 │  │ Modules │ │
│  └─────────────────┘  └─────────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка конфигурации

```bash
# Скопируйте пример конфигурации
cp env.example config.env

# Отредактируйте config.env файл с вашими настройками
# ВАЖНО: Токен бота уже настроен в config.env
# НЕ ДЕЛИТЕСЬ ТОКЕНОМ БОТА!
```

### 3. Запуск бота

```bash
# Режим polling
python alert_bot.py

# Режим webhook
python alert_bot.py webhook
```

### 4. Docker запуск

```bash
docker-compose up -d
```

## ⚙️ Конфигурация

### Основные настройки

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `BOT_TOKEN` | Токен Telegram бота | - |
| `WEBHOOK_SECRET` | Секретный ключ для webhook | - |
| `ALERT_CHAT_ID` | ID чата для алертов | - |
| `DATABASE_URL` | URL базы данных | `sqlite:///data/alerts.db` |
| `ALERT_COOLDOWN` | Задержка между алертами (сек) | 60 |
| `MAX_ALERTS_PER_HOUR` | Максимум алертов в час | 100 |

### Настройки модулей

```python
MONITORED_MODULES = [
    "TeBium-Analytics-Server",
    "Telegram-Bot-Tebium", 
    "TeBium-Alert-Bot"
]
```

## 📡 API для интеграции

### Отправка алерта через HTTP

```bash
curl -X POST http://localhost:8082/webhook/your-secret \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret" \
  -d '{
    "type": "error",
    "priority": "critical",
    "module": "MyModule",
    "message": "Критическая ошибка!",
    "data": {"error_code": 500}
  }'
```

### Отправка алерта через Python

```python
import asyncio
from alert_bot import TeBiumAlertBot

async def send_alert():
    bot = TeBiumAlertBot()
    await bot.send_system_alert(
        alert_type="error",
        message="Что-то пошло не так",
        priority="warning",
        module="MyModule"
    )

asyncio.run(send_alert())
```

## 🎮 Команды бота

### Пользовательские команды
- `/start` - Главное меню
- `/help` - Справка
- `/status` - Статус системы
- `/stats` - Статистика алертов
- `/ping` - Проверка связи
- `/test` - Отправка тестового алерта

### Административные команды
- `/admin` - Панель администратора
- Управление модулями
- Просмотр истории алертов
- Настройка системы

## 🔧 Разработка

### Структура проекта

```
TeBium-Alert-Bot/
├── alert_bot.py              # Основной файл бота
├── config/                   # Конфигурация
│   ├── settings.py           # Настройки
│   └── alert_templates.py    # Шаблоны сообщений
├── handlers/                 # Обработчики команд
│   ├── admin_handlers.py     # Админ команды
│   ├── alert_handlers.py     # Обработка алертов
│   └── system_handlers.py    # Системные команды
├── utils/                    # Утилиты
│   ├── database.py           # Работа с БД
│   ├── alert_manager.py      # Менеджер алертов
│   └── logger.py             # Логирование
├── scripts/                  # Скрипты
├── data/                     # Данные
├── logs/                     # Логи
└── tests/                    # Тесты
```

### Запуск тестов

```bash
pytest tests/
```

### Линтинг

```bash
black .
flake8 .
mypy .
```

## 📊 Мониторинг

### Метрики
- Количество отправленных алертов
- Время ответа модулей
- Статус здоровья системы
- Статистика по типам алертов

### Логи
- Структурированное логирование
- Ротация логов
- Отдельные файлы для ошибок

## 🔒 Безопасность

### ⚠️ ВАЖНО: Токен бота защищен!
- **Токен бота**: `8354021077:AAFKnwLGblJggn4qpgxnfnw4Msw8jsbTsMg`
- **НИКОГДА НЕ ДЕЛИТЕСЬ ТОКЕНОМ!**
- **Webhook аутентификация** через секретный токен
- **Rate limiting** для предотвращения спама
- **Валидация данных** входящих алертов
- **Изоляция в Docker** контейнере
- **Файлы конфигурации** исключены из Git

### 🛡️ Меры безопасности
- Конфигурация в `config.env` (не в Git)
- Автоматическая генерация webhook секретов
- Проверка прав доступа к файлам
- Безопасный запуск через `scripts/secure_start.py`

Подробнее см. [SECURITY.md](SECURITY.md)

## 🚀 Развертывание

### Docker Compose

```yaml
version: '3.8'
services:
  alert-bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - WEBHOOK_SECRET=${WEBHOOK_SECRET}
    ports:
      - "8082:8082"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tebium-alert-bot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tebium-alert-bot
  template:
    metadata:
      labels:
        app: tebium-alert-bot
    spec:
      containers:
      - name: alert-bot
        image: tebium/alert-bot:latest
        ports:
        - containerPort: 8082
        env:
        - name: BOT_TOKEN
          valueFrom:
            secretKeyRef:
              name: telegram-secret
              key: bot-token
```

## 🤝 Интеграция с другими модулями

### TeBium-Analytics-Server
```python
# Отправка алерта о проблемах с аналитикой
await send_alert({
    "type": "performance",
    "priority": "warning",
    "module": "TeBium-Analytics-Server",
    "message": "Высокая нагрузка на сервер",
    "data": {"cpu_usage": 85, "memory_usage": 90}
})
```

### Telegram-Bot-Tebium
```python
# Отправка алерта о проблемах с основным ботом
await send_alert({
    "type": "error",
    "priority": "critical",
    "module": "Telegram-Bot-Tebium",
    "message": "Бот не отвечает на команды",
    "data": {"last_response": "5 minutes ago"}
})
```

## 📈 Планы развития

- [ ] **Web интерфейс** для управления алертами
- [ ] **Интеграция с Prometheus** для метрик
- [ ] **Поддержка Slack/Discord** уведомлений
- [ ] **Машинное обучение** для классификации алертов
- [ ] **Автоматическое исправление** простых проблем
- [ ] **Географическое распределение** алертов

## 🐛 Известные проблемы

- При высокой нагрузке возможны задержки в отправке алертов
- SQLite может стать узким местом при большом количестве алертов
- Webhook может быть недоступен при перезапуске бота

## 📞 Поддержка

Для получения помощи:
1. Проверьте логи в папке `logs/`
2. Используйте команду `/admin` для диагностики
3. Обратитесь к администратору системы

## 📄 Лицензия

Этот проект является частью экосистемы TeBium и распространяется под лицензией MIT.

## 🔗 Ссылки

- **Репозиторий**: [GitHub](https://github.com/TigranWQ/tebium-alert-bot)
- **Экосистема**: [ECOSYSTEM.md](ECOSYSTEM.md)
- **Безопасность**: [SECURITY.md](SECURITY.md)
- **Быстрый старт**: [QUICK_START.md](QUICK_START.md)

---

**TeBium Alert Bot** - надежный страж вашей системы! 🚨
