# 🚀 Быстрый старт TeBium Alert Bot

## ⚠️ ВАЖНО: Безопасность

**Токен бота уже настроен**: `8354021077:AAFKnwLGblJggn4qpgxnfnw4Msw8jsbTsMg`

**НИКОГДА НЕ ДЕЛИТЕСЬ ЭТИМ ТОКЕНОМ!**

## 🎯 Быстрый запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка (уже готово!)

Конфигурация уже настроена в `config.env`:
- ✅ Токен бота установлен
- ✅ Webhook секрет сгенерирован
- ✅ База данных настроена
- ✅ Логирование настроено

### 3. Запуск бота

#### Windows (PowerShell)
```powershell
.\run_bot.ps1
```

#### Windows (Batch)
```cmd
run_bot.bat
```

#### Linux/macOS
```bash
python scripts/secure_start.py
```

#### Docker
```bash
docker-compose up -d
```

## 🔧 Настройка чата для алертов

1. **Создайте группу** в Telegram
2. **Добавьте бота** в группу
3. **Получите ID чата**:
   - Отправьте сообщение в группу
   - Перейдите по ссылке: `https://api.telegram.org/bot8354021077:AAFKnwLGblJggn4qpgxnfnw4Msw8jsbTsMg/getUpdates`
   - Найдите `"chat":{"id":-123456789}` - это ваш ID чата
4. **Обновите config.env**:
   ```bash
   ALERT_CHAT_ID=-123456789
   ```

## 🧪 Тестирование

### Отправка тестового алерта
```bash
python scripts/send_test_alert.py
```

### Проверка статуса
```bash
# В Telegram отправьте команду
/start
/status
/stats
```

### Проверка webhook
```bash
curl -X POST http://localhost:8082/webhook/your-secret \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret" \
  -d '{
    "type": "test",
    "priority": "info",
    "module": "test-module",
    "message": "Test webhook message"
  }'
```

## 📊 Мониторинг

### Логи
```bash
# Просмотр логов
tail -f logs/alert_bot.log

# Логи ошибок
tail -f logs/error_*.log
```

### База данных
```bash
# SQLite база данных
sqlite3 data/alerts.db

# Просмотр алертов
SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 10;
```

### Статистика
- Отправьте `/stats` в Telegram
- Используйте `/admin` для административной панели

## 🔒 Безопасность

### Проверка безопасности
```bash
python scripts/secure_start.py
```

### Ротация секретов
```bash
# Webhook секрет автоматически генерируется
# При необходимости обновите в config.env
```

### Бэкап
```bash
# Бэкап базы данных
cp data/alerts.db backups/alerts_$(date +%Y%m%d).db

# Бэкап конфигурации
cp config.env backups/config_$(date +%Y%m%d).env
```

## 🚨 Устранение проблем

### Бот не запускается
1. Проверьте токен бота
2. Проверьте права доступа к файлам
3. Проверьте логи: `logs/alert_bot.log`

### Алерты не приходят
1. Проверьте ID чата в config.env
2. Убедитесь, что бот добавлен в группу
3. Проверьте права бота в группе

### Webhook не работает
1. Проверьте webhook секрет
2. Убедитесь, что порт 8082 свободен
3. Проверьте firewall настройки

## 📞 Поддержка

При проблемах:
1. Проверьте логи
2. Используйте `/admin` в Telegram
3. Обратитесь к администратору

## 🎉 Готово!

Ваш TeBium Alert Bot готов к работе! 🚨

**Следующие шаги:**
1. Настройте ID чата для алертов
2. Протестируйте отправку алертов
3. Настройте мониторинг других модулей
4. Настройте автоматические проверки

---

**Удачного мониторинга!** 📊✨
