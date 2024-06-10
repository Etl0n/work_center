import os

import psycopg2 as ps
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

from access_db import get_content, insert_data
from models import db

load_dotenv()

app = Flask(__name__)


username = os.getenv("USER", "postgres")
password = os.getenv("PASSWORD", "")
dbname = os.getenv("DATABASE", "")
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql://{username}:{password}@localhost:5432/{dbname}'
)
app.config['DEBUG'] = False

LIST_DATABASE = [
    "personal_data",
    "education",
    "passport_data",
    "regperson",
    "vacancy",
    "the_worst_vacancy",
    "free_vacancy",
    "the_best_salary",
    # "crosstab_before_claster",
]


# Параметры подключения к БД
DATABASE = {
    "host": os.getenv("HOST", "localhost"),
    "port": os.getenv("PORT", 5432),
    "database": os.getenv("DATABASE", ""),
    "user": os.getenv("USER", "postgres"),
    "password": os.getenv("PASSWORD", ""),
}


# Подключение к БД
try:
    conn = ps.connect(**DATABASE)
    conn.autocommit = True
    print(
        'Вы подключены к базе данных "center_work" как пользователь "postgres".'
    )
except ps.OperationalError:
    print("Can`t establish connection to  databse")
    raise


try:
    conn.cursor().execute('CREATE SCHEMA centre_work')
except ps.errors.DuplicateSchema:
    print('Схема с названием centre_work уже создана')

# Создание таблиц
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template(
        "menu.html", name_database="Главаное меню", list_database=LIST_DATABASE
    )


@app.route("/personal_data/", methods=["GET"])
def personal_data():
    if request.method == "GET":
        data = []
        # Название столбцов для вывода
        data.append(
            tuple(
                [
                    "joblessid",
                    "lastname",
                    "firstname",
                    "patronymic",
                    "age",
                    "passport",
                    "address",
                    "phone",
                    "picture",
                    "payment",
                    "experience",
                ]
            )
        )
        # Получение данных из таблиц, данная функция импортирована из дургого файла
        data += get_content(conn=conn, database="personal_data")
        return render_template("personaldata.html", data=data)


@app.route("/education/")
def education():
    if request.method == "GET":
        data = []
        # Название столбцов для вывода
        data.append(
            tuple(
                ["id", "joblessid", "studyplace", "studyaddress", "studytype"]
            )
        )
        # Получение данных из таблиц, данная функция импортирована из дургого файла
        data += get_content(conn=conn, database="education")
        return render_template("viewlist.html", data=data, add_form=False)


@app.route("/passport_data/")
def passportdata():
    if request.method == "GET":
        data = []
        # Название столбцов для вывода
        data.append(tuple(["id", "passport", "passportdate", "region"]))
        # Получение данных из таблиц, данная функция импортирована из дургого файла
        data += get_content(conn=conn, database="passport_data")
        return render_template("viewlist.html", data=data, add_form=False)


@app.route("/regperson/")
def regperson():
    if request.method == "GET":
        data = []
        # Название столбцов для вывода
        data.append(
            tuple(
                [
                    "id",
                    "idreg",
                    "registrar",
                    "regdate",
                    "arhivist",
                    "archivesdate",
                    "active",
                    "vacancy",
                ]
            )
        )
        # Получение данных из таблиц, данная функция импортирована из дургого файла
        data += get_content(conn=conn, database="regperson")
        return render_template("viewlist.html", data=data, add_form=True)


@app.route("/vacancy/")
def vacancy():
    if request.method == "GET":
        data = []
        # Название столбцов для вывода
        data.append(
            tuple(
                [
                    "jobid",
                    "jobtype",
                    "jobname",
                    "jobgiver",
                    "place",
                    "mobile",
                    "district",
                    "money",
                    "more",
                    "active",
                ]
            )
        )
        # Получение данных из таблиц, данная функция импортирована из дургого файла
        data += get_content(conn=conn, database="vacancy")
        return render_template("viewlist.html", data=data, add_form=True)


# первый доп запрос
@app.route("/the_worst_vacancy/", methods=["GET"])
def the_worst_vacancy():
    cursor = conn.cursor()
    data = []
    data.append(tuple(["jobname", "count"]))
    cursor.execute(
        "with cte as (SELECT v.jobname, COUNT(*) as count "
        "FROM centre_work.regperson as r "
        "JOIN centre_work.vacancy as v ON r.vacancy=v.jobid "
        "GROUP BY v.jobname) "
        "SELECT v.jobname, cte.count "
        "FROM centre_work.vacancy as v "
        "JOIN cte ON v.jobname=cte.jobname "
        "WHERE cte.count=(SELECT MAX(cte.count) "
        "FROM cte)"
    )
    data.extend(cursor.fetchall())
    cursor.close()
    return render_template("viewlist.html", data=data, add_form=False)


# второй доп запрос
@app.route("/free_vacancy/", methods=["GET"])
def free_vacancy():
    cursor = conn.cursor()
    data = []
    data.append(
        tuple(
            [
                "jobid",
                "jobtype",
                "jobname",
                "jobgiver",
                "place",
                "mobile",
                "district",
                "money",
                "more",
                "active",
            ]
        )
    )
    cursor.execute("SELECT * FROM centre_work.vacancy WHERE active=True")
    data.extend(cursor.fetchall())
    cursor.close()
    return render_template("viewlist.html", data=data, add_form=False)


# третий доп запрос
@app.route("/the_best_salary/", methods=["GET"])
def the_best_salary():
    cursor = conn.cursor()
    data = []
    data.append(
        tuple(
            [
                "jobid",
                "jobtype",
                "jobname",
                "jobgiver",
                "place",
                "mobile",
                "district",
                "money",
                "more",
                "active",
            ]
        )
    )
    cursor.execute(
        "SELECT * FROM centre_work.vacancy as v "
        "WHERE v.money=(SELECT MAX(v.money) "
        "FROM centre_work.vacancy as v)"
    )
    data.extend(cursor.fetchall())
    cursor.close()
    return render_template("viewlist.html", data=data, add_form=False)


# четвертый запрос, в доработке
@app.route("/crosstab_before_claster/", methods=["GET"])
def crosstab_before_claster():
    cursor = conn.cursor()
    cursor.execute(
        "SELECT "
        "CASE "
        "WHEN money < 20000 THEN 'Кластер 1: < 20000' "
        "WHEN money >= 20000 AND money < 40000 THEN 'Кластер 2: 20000-39999' "
        "WHEN money >= 40000 AND money < 60000 THEN 'Кластер 3: 40000-59999' "
        "WHEN money >= 60000 AND money < 80000 THEN 'Кластер 4: 60000-79999' "
        "ELSE 'Кластер 5: >= 80000' "
        "END AS salary_cluster, "
        "CASE "
        "WHEN place='Удаленно' THEN 'удаленно' "
        "ELSE 'оффис' "
        "END AS work_type, "
        "COUNT(*) AS count_vacancy "
        "FROM centre_work.vacancy "
        "WHERE active='True' "
        "GROUP BY salary_cluster, work_type "
        "ORDER BY salary_cluster, work_type "
    )
    data = cursor.fetchall()
    new_data = list()
    new_data.append(
        tuple(
            [
                "№ Кластера",
                "Оффис",
                "Удаленно",
            ]
        )
    )
    new_data.append(tuple([data[0][0], data[0][2], data[1][2]]))
    new_data.append(tuple([data[2][0], data[2][2], data[3][2]]))
    new_data.append(tuple([data[4][0], data[4][2], data[5][2]]))
    new_data.append(tuple([data[6][0], data[6][2], data[7][2]]))
    new_data.append(tuple([data[8][0], data[8][2], data[9][2]]))
    cursor.close()
    return render_template("viewlist.html", data=new_data, add_form=False)


@app.route("/personal_data/form/", methods=["POST", "GET"])
def add_personal():
    # Вывод формы
    if request.method == "GET":
        fields = {
            "Имя": "firstname",
            "Фамилия": "lastname",
            "Отчество": "patronymic",
            "Возраст": "age",
            "Адресс": "address",
            "Номер телефона": "phone",
            "Ссылка на фотографию": "picture",
            "Желаемая зарплата": "payment",
            "Номер паспора": "passport",
            "Дата регистрации паспорта": "passportdate",
            "Место регитрации паспорта": "region",
        }
        return render_template(
            "form.html", fields=fields, table="personal_data"
        )
    if request.method == "POST":
        keys = list(request.form.keys())
        column_for_personaldata = keys[:-4:]
        column_for_personaldata.extend([keys[-1], keys[-4]])
        values_for_personaldata = [
            request.form[x] for x in column_for_personaldata
        ]
        column_for_passportdata = keys[-4:-1:]
        values_for_passportdata = [
            request.form[x] for x in column_for_passportdata
        ]
        column_for_personaldata = ", ".join(column_for_personaldata)
        column_for_passportdata = ", ".join(column_for_passportdata)

        insert_data(
            conn=conn,
            database="passport_data",
            column=column_for_passportdata,
            values=values_for_passportdata,
        )
        insert_data(
            conn=conn,
            database="personal_data",
            column=column_for_personaldata,
            values=values_for_personaldata,
        )
        return redirect(url_for("personal_data"))


@app.route("/vacancy/form/", methods=["POST", "GET"])
def add_vacancy():
    # Вывод формы
    if request.method == "GET":
        fields = {
            "Тип вакансии": "jobtype",
            "Название вакансии": "jobname",
            "Работадель": "jobgiver",
            "Адрес работадателя": "place",
            "Телефон работадателя": "mobile",
            "Район в котором предоставляется работа": "district",
            "Зарплата": "money",
            "Доп информация": "more",
        }
        return render_template("form.html", fields=fields, table="vacancy")

    # Обрботка полученных данных
    if request.method == "POST":
        keys = list(request.form.keys())
        column = ", ".join(keys)
        values = [request.form[x] for x in keys]
        insert_data(
            conn=conn, database="vacancy", column=column, values=values
        )
        return redirect(url_for("vacancy"))


@app.route("/regperson/form/", methods=["POST", "GET"])
def add_regperson():
    # Вывод формы
    if request.method == "GET":
        fields = {
            "ID пользователя": "id",
            "Фамилия регистрирующего": "registrar",
            "Дата постановки на учет": "regdate",
            "Фамилия добавившего в архив": "archivist",
            "Дата добавления в архив": "archivesdate",
            "Вакансия": "vacancy",
        }
        return render_template("form.html", fields=fields, table="regperson")

    # Обрботка полученных данных
    if request.method == "POST":
        keys = list(request.form.keys())
        values = [request.form[x] for x in keys]
        keys.append("idreg")
        column = ", ".join(keys)
        insert_data(
            conn=conn, database="regperson", column=column, values=values
        )
        return redirect(url_for("regperson"))


if __name__ == "__main__":
    app.run("127.0.0.1", port="8000")
