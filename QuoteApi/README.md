QuoteAPI
Инструкция по развертыванию проекта

Создать виртуальное окружение
python3 -m venv flask_venv

Активировать виртуальное окружение
source flask_venv/bin/activate

Установить нужные библиотеки
python -m pip install -r requirements.txt

Применить миграции
flask db upgrade

Создаем файл .flaskenv:
FLASK_APP=run.py
FLASK_DEBUG=1

Запускаем приложение:
flask run