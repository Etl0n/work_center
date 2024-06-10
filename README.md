# Work-Center
[![Python](https://img.shields.io/badge/-Python-090909?style=for-the-badge&logo=Python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-090909?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlhemy-090909?style=for-the-badge&logo=SQLAlhemy)](https://flask-sqlalchemy.palletsprojects.com/en/latest/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-090909?style=for-the-badge&logo=PostgreSQL)](https://www.postgresql.org/)
### Описание проекта:
---
Work-center – это платформа, на которой работодатель и соискатели могут взаимодействовать и находить подходящих кандидатов на вакансии. Она имеет существенное значение как для работодателей, так и для соискателей, упрощая и ускоряя процесс подбора персонала и поиска работы. При помощи трех дополнительных запросов произоводится выборки. Используется СУБД PostgreSql взаимодействие с ней идет при помощи библиотеки psycopg2-binary(Первый проект написанный при помощи Flask)

### Технологии, которые использовались:
---
- Python
- Flask
- FlaskSqlAlchemy
- PostgreSQL

### Как установить проект:
Клонировать репозиторий и перейти в него в командной строке:

- > git clone git@github.com:Etl0n/work_center.git
- > cd work_center

Cоздать и активировать виртуальное окружение:

- > python -m venv venv
- > source venv/Source/activate

Установить зависимости из файла requirements.txt:

- > python -m pip install --upgrade pip
- > pip install -r requirements.txt

Настроить подключение к БД PostgreSQL:

- > Создать в директории файл .env c таким текстом
```
DATABASE='{название уже созданной пустой БД}'
PASSWORD='{пароль от вашей БД}'
``` 
Запустить приложение

- > python main.py

### Планы
---
- [x] Автоматизировать создание таблиц в БД, так как сейчас их нужно создавать в ручную при помощи (psql или PgAdmin4)
На данный момент не возможно удобно воспользоваться приложением.(Данной проблемы больше нет)
- [ ] Переписать все запросы к БД при помощи SQLAlchemy(то есть без использования psycopg2-binary)

### Автор
[Etl0n](https://github.com/Etl0n) (PythonDeveloper)