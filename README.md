# Mouse.NET VPN Bot 🐭

Telegram-бот для VPN-сервиса Mouse.NET.

## 1. Получение BOT_TOKEN

1. Откройте Telegram и найдите @BotFather
2. Отправьте команду `/newbot`
3. Следуйте инструкциям, укажите имя бота (например, `MouseNET VPN Bot`)
4. После создания BotFather выдаст токен — сохраните его

## 2. Заполнение .env

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```
BOT_TOKEN=ваш_токен_от_BotFather
ADMIN_IDS=ваш_telegram_id (можно получить у @userinfobot)
```

Несколько админов через запятую: `123456789,987654321`

## 3. Запуск локально

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
python main.py
```

## 4. Заливка на GitHub

```bash
git init
git add .
git commit -m "Initial commit: Mouse.NET VPN Bot"
git remote add origin https://github.com/ВАШ_ЛОГИН/mousenet-bot.git
git branch -M main
git push -u origin main
```

## 5. Деплой на Render

1. Зайдите на [Render](https://dashboard.render.com)
2. Нажмите **New +** → **Blueprint**
3. Подключите ваш GitHub-репозиторий
4. Render автоматически найдёт `render.yaml` и настроит сервис
5. После деплоя добавьте секреты (см. шаг 6)
6. Нажмите **Manual Deploy** → **Deploy latest commit**

## 6. Переменные окружения в Render

В панели Render (Dashboard → ваш сервис → Environment) добавьте:

| Ключ | Значение |
|------|----------|
| `BOT_TOKEN` | Токен от @BotFather (секрет) |
| `ADMIN_IDS` | Telegram ID администраторов (через запятую) |

**Не коммитьте `.env` в репозиторий!** Все секреты задаются через Environment Variables на Render.

## Структура проекта

```
mousenet_bot/
├── main.py              # Точка входа
├── config.py            # Конфигурация (env)
├── database.py          # Работа с SQLite
├── keyboards.py         # Клавиатуры
├── handlers/
│   ├── __init__.py
│   ├── start.py         # /start
│   ├── tariffs.py       # Тарифы и оплата
│   ├── trial.py         # Пробный период
│   ├── servers.py       # Серверы
│   ├── referral.py      # Реферальная система
│   ├── contest.py       # Конкурс
│   ├── support.py       # Поддержка
│   └── admin.py         # Админ-панель
├── requirements.txt
├── render.yaml
├── .env.example
└── README.md
```
