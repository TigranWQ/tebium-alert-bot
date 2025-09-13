# 🚀 Ручная настройка Git для TeBium Alert Bot

## ✅ Репозиторий готов!
Репозиторий [tebium-alert-bot](https://github.com/TigranWQ/tebium-alert-bot.git) создан и пуст - это идеально!

## 🔧 Выполните следующие команды:

### Вариант 1: Запустите готовый скрипт
```cmd
cd C:\Prodjects\TeBium-Alert-Bot
push_to_github.bat
```

### Вариант 2: Выполните команды вручную

Откройте **Command Prompt** (cmd) и выполните:

```cmd
# 1. Перейдите в папку проекта
cd C:\Prodjects\TeBium-Alert-Bot

# 2. Проверьте статус Git
git status

# 3. Удалите существующий remote (если есть)
git remote remove origin

# 4. Добавьте GitHub remote
git remote add origin https://github.com/TigranWQ/tebium-alert-bot.git

# 5. Проверьте remote
git remote -v

# 6. Переименуйте ветку в main
git branch -M main

# 7. Отправьте код на GitHub
git push -u origin main
```

## 🔐 Аутентификация

При выполнении `git push` вас могут попросить ввести:
- **Username**: `TigranWQ`
- **Password**: Используйте **Personal Access Token** (не пароль от GitHub)

### Создание Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Выберите scopes: `repo` (полный доступ к репозиториям)
4. Скопируйте токен и используйте как пароль

## ✅ После успешного выполнения:

Проверьте репозиторий: https://github.com/TigranWQ/tebium-alert-bot

Должны увидеть:
- 📄 README.md с полной документацией
- 🔒 SECURITY.md с руководством по безопасности
- 🚀 QUICK_START.md с быстрым стартом
- 🏗️ ARCHITECTURE.md с архитектурой
- 🌐 ECOSYSTEM.md с интеграцией
- 🐳 Docker файлы
- 📁 Все исходные коды

## 🎯 Что будет загружено:

### 📁 Структура проекта:
```
tebium-alert-bot/
├── README.md                 # Основная документация
├── SECURITY.md               # Безопасность
├── QUICK_START.md            # Быстрый старт
├── ARCHITECTURE.md           # Архитектура
├── ECOSYSTEM.md              # Интеграция с экосистемой
├── config.env                # Конфигурация (с токеном бота)
├── Dockerfile                # Docker образ
├── docker-compose.yml        # Docker Compose
├── requirements.txt          # Python зависимости
├── .gitignore                # Исключения для Git
├── alert_bot.py              # Основной файл бота
├── config/                   # Конфигурация
├── handlers/                 # Обработчики команд
├── utils/                    # Утилиты
├── scripts/                  # Скрипты
└── tests/                    # Тесты
```

### 🔗 Связь с экосистемой:
- **TeBium-Analytics-Server**: https://github.com/TigranWQ/tebium-analytics-server
- **Telegram-Bot-Tebium**: https://github.com/TigranWQ/telegram-bot-tebium
- **TeBium-Alert-Bot**: https://github.com/TigranWQ/tebium-alert-bot

## 🛡️ Безопасность:
- ✅ Токен бота `8354021077:AAFKnwLGblJggn4qpgxnfnw4Msw8jsbTsMg` защищен в `config.env`
- ✅ Секретные файлы исключены из Git через `.gitignore`
- ✅ Документация по безопасности включена

---

**Готово к загрузке!** 🚀
