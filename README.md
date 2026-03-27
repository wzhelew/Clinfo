# Clinfo

Малко Flask уеб приложение за вход на потребители и преглед на техните:
- фактури
- стокови наличности
- задължения

## Къде е базата?
Самата MySQL база (данните) не стои в Git. В Git добавих:
- `db/schema.sql` (структура на таблиците)
- `docker-compose.yml` (локален MySQL контейнер)

## Изисквания
- Python 3.11+
- MySQL 8+

## Вариант A: Бърз старт с Docker
```bash
docker compose up -d
```

## Вариант B: Ръчен импорт на структура
```bash
mysql -u root -p < db/schema.sql
```

## Стартиране
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Попълни `.env` с реални данни за MySQL.

Пример:
```env
DATABASE_URL=mysql+pymysql://clinfo:clinfo123@127.0.0.1:3306/clinfo
SECRET_KEY=change-this
```

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
