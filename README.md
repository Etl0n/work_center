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

### Планы
---
- [x] Автоматизировать создание таблиц в БД, так как сейчас их нужно создавать в ручную при помощи (psql или PgAdmin4)
На данный момент не возможно удобно воспользоваться приложением.
- [ ] Переписать все запросы к БД при помощи SQLAlchemy(то есть без использования psycopg2-binary)

### Автор
[Etl0n](https://github.com/Etl0n) (Ученик Яндекс Практикума)