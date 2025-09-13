# 🔒 Безопасность TeBium Alert Bot

## ⚠️ ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ

### 🚨 Токен бота
**НИКОГДА НЕ ДЕЛИТЕСЬ ТОКЕНОМ БОТА!**

Текущий токен: `8354021077:AAFKnwLGblJggn4qpgxnfnw4Msw8jsbTsMg`

Если токен скомпрометирован:
1. Немедленно отзовите токен в @BotFather
2. Создайте новый токен
3. Обновите `config.env` файл
4. Перезапустите бота

### 🛡️ Меры безопасности

#### 1. Файлы конфигурации
- ✅ `config.env` - содержит секретные данные
- ❌ НЕ добавляйте в Git
- ✅ Используйте `.gitignore`
- ✅ Регулярно ротируйте секреты

#### 2. Webhook безопасность
- ✅ Используйте HTTPS для webhook
- ✅ Секретный токен для аутентификации
- ✅ Валидация входящих данных
- ✅ Rate limiting

#### 3. База данных
- ✅ SQLite файл в защищенной папке
- ✅ Регулярные бэкапы
- ✅ Шифрование чувствительных данных

#### 4. Логирование
- ✅ Не логируйте секретные данные
- ✅ Ротация логов
- ✅ Мониторинг подозрительной активности

## 🔐 Рекомендации по безопасности

### 1. Переменные окружения
```bash
# Создайте отдельный файл для продакшена
cp config.env config.prod.env

# Установите правильные права доступа
chmod 600 config.prod.env

# Используйте системные переменные окружения
export BOT_TOKEN="your_token_here"
```

### 2. Docker безопасность
```dockerfile
# Используйте non-root пользователя
USER alertbot

# Не копируйте секретные файлы в образ
# Используйте secrets или environment variables
```

### 3. Сетевая безопасность
- Используйте VPN для доступа к серверу
- Настройте firewall
- Используйте reverse proxy (nginx)
- Включите SSL/TLS

### 4. Мониторинг
- Отслеживайте подозрительную активность
- Мониторьте использование ресурсов
- Настройте алерты о безопасности

## 🚨 Процедуры при инцидентах

### 1. Компрометация токена
1. Немедленно отзовите токен в @BotFather
2. Создайте новый токен
3. Обновите конфигурацию
4. Перезапустите все сервисы
5. Проверьте логи на подозрительную активность

### 2. Компрометация сервера
1. Изолируйте сервер
2. Смените все пароли и токены
3. Проверьте целостность данных
4. Восстановите из бэкапа
5. Проведите аудит безопасности

### 3. DDoS атака
1. Включите rate limiting
2. Используйте CDN
3. Блокируйте подозрительные IP
4. Масштабируйте ресурсы

## 📋 Чек-лист безопасности

### Перед развертыванием
- [ ] Токен бота защищен
- [ ] Webhook использует HTTPS
- [ ] Секретные файлы в .gitignore
- [ ] Настроен firewall
- [ ] Включено логирование
- [ ] Настроен мониторинг

### Регулярно (еженедельно)
- [ ] Проверка логов на аномалии
- [ ] Обновление зависимостей
- [ ] Проверка прав доступа к файлам
- [ ] Ротация логов
- [ ] Бэкап базы данных

### При подозрениях
- [ ] Немедленная смена токенов
- [ ] Проверка логов
- [ ] Анализ сетевого трафика
- [ ] Уведомление администраторов
- [ ] Документирование инцидента

## 🔧 Настройка безопасного развертывания

### 1. Создание безопасного пользователя
```bash
# Создайте отдельного пользователя для бота
sudo useradd -m -s /bin/bash alertbot
sudo usermod -aG docker alertbot

# Создайте директорию для бота
sudo mkdir -p /opt/tebium-alert-bot
sudo chown alertbot:alertbot /opt/tebium-alert-bot
```

### 2. Настройка файлов
```bash
# Установите правильные права
chmod 600 config.env
chmod 700 data/
chmod 700 logs/

# Создайте символическую ссылку
ln -s /opt/tebium-alert-bot/config.env /path/to/bot/config.env
```

### 3. Systemd сервис
```ini
[Unit]
Description=TeBium Alert Bot
After=network.target

[Service]
Type=simple
User=alertbot
WorkingDirectory=/opt/tebium-alert-bot
ExecStart=/usr/bin/python3 alert_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. Nginx конфигурация
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location /webhook/ {
        proxy_pass http://localhost:8082;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📞 Контакты для безопасности

При обнаружении уязвимостей:
1. НЕ создавайте публичные issue
2. Свяжитесь с администратором системы
3. Предоставьте детали уязвимости
4. Дождитесь исправления

## 📚 Дополнительные ресурсы

- [Telegram Bot API Security](https://core.telegram.org/bots/api#security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)

---

**Помните: Безопасность - это процесс, а не состояние!** 🔒
