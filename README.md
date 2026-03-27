# Clinfo

Малко Flask уеб приложение за вход на потребители и преглед на техните:
- фактури
- стокови наличности
- задължения

## Изисквания
- Python 3.11+
- MySQL 8+

## Стартиране
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Попълни `.env` с реални данни за MySQL.

### Инициализация
```bash
flask --app app init-db
flask --app app create-user
```

### Пускане
```bash
flask --app app run --debug
```

Отвори: `http://127.0.0.1:5000`

## База данни (примерни таблици)
Приложението използва таблици:
- `users`
- `invoices`
- `stock_items`
- `debts`

Ако вече имаш таблици, можеш да адаптираш SQLAlchemy моделите в `app.py` към твоята структура.
