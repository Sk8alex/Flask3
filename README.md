Flask2_25052025
Развертывание на локальной машине
Создаем виртуальное окружение: python3 -m venv flask_venv
Активируем venv: source flask_venv/bin/activate
Устанавливаем зависимости: pip install -r requirements.txt
Создаем локальную БД: flask db upgrade
Запускаем приложение: python run.py
Ссылка на документацию
Настройки для запуска flask run тут https://flask.palletsprojects.com/en/stable/cli/
Настройки для конфигов тут https://flask.palletsprojects.com/en/stable/config/


Работа с sqlite3
Установка CLI для sqlite:
sudo apt install sqlite3
Создать дамп БД (схема + данные):
sqlite3 quotes.db .dump > db_sql/db_data.sql
Создать дамп БД (только схема):
sqlite3 quotes.db ".schema quotes" > db_sql/db_schema.sql
Загрузить данные в БД:
sqlite3 new_store.db ".read db_sql/db_data.sql"