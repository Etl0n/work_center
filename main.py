import os

import psycopg2 as ps
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from access_db import get_content, insert_data

load_dotenv()

app = Flask(__name__)

username = os.getenv("USER", "postgres")
password = os.getenv("PASSWORD", "")
dbname = os.getenv("DATABASE", "")
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql://{username}:{password}@localhost:5432/{dbname}'
)
app.config['DEBUG'] = True


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


db = SQLAlchemy(app)


class PassportData(db.Model):
    __table_args__ = {'schema': 'centre_work'}
    id = db.Column(db.Integer, primary_key=True)
    passport = db.Column(db.Integer, nullable=True, unique=True)
    passport_date = db.Column(db.Date, nullable=True)
    region = db.Column(db.String(100), nullable=True)
    personal = db.relationship('PersonalData', back_populates='passport')


class PersonalData(db.Model):
    __table_args__ = {'schema': 'centre_work'}
    joblessid = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(100), nullable=True)
    firstname = db.Column(db.String(100), nullable=True)
    patronymic = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    passport = db.Column(
        db.Integer, db.ForeignKey('centre_work.passport_data.passport')
    )
    passport_rel = db.relationship(
        'PassportData', uselist=False, back_populates='personal'
    )
    education = db.relationship('Education', back_populates='personal')
    address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    picture = db.Column(db.String(100), nullable=True)
    payment = db.Column(db.String(100), nullable=True)
    experience = db.Column(db.Boolean, nullable=True)


class Education(db.Model):
    __table_args__ = {'schema': 'centre_work'}
    id = db.Column(db.Integer, primary_key=True)
    joblessid = db.Column(
        db.Integer, db.ForeignKey('centre_work.personal_data.joblessid')
    )
    studyaddress = db.Column(db.String(100), nullable=True)
    studytype = db.Column(db.String(100), nullable=True)


class Vacancy(db.Model):
    __table_args__ = {'schema': 'centre_work'}
    jobid = db.Column(db.Integer, primary_key=True)
    jobtype = db.Column(db.String(100), nullable=True)
    jobname = db.Column(db.String(100), nullable=True)
    jobgiver = db.Column(db.String(100), nullable=True)
    place = db.Column(db.String(100), nullable=True)
    mobile = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    money = db.Column(db.Integer, nullable=True)
    more = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True)


with app.app_context():
    db.create_all()

LIST_DATABASE = [
    "personaldata",
    "education",
    "passportdata",
    "regperson",
    "vacancy",
    "the_worst_vacancy",
    "free_vacancy",
    "the_best_salary",
]


@app.route("/")
def index():
    return render_template(
        "menu.html", name_database="Главаное меню", list_database=LIST_DATABASE
    )


@app.route("/personaldata/", methods=["GET"])
def personaldata():
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


@app.route("/passportdata/")
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


@app.route("/personaldata/form/", methods=["POST", "GET"])
def add_personal():
    # Вывод формы
    if request.method == "GET":
        fields = {
            "Имя": "firstname",
            "Фамилия": "lastname",
            "Отчество": "patronymic",
            "Возраст": "age",
            "Номер паспора": "passport",
            "Адресс": "address",
            "Номер телефона": "phone",
            "Ссылка на фотографию": "picture",
            "Желаемая зарплата": "payment",
            "Дата регистрации паспорта": "passportdate",
            "Место регитрации паспорта": "region",
        }
        return render_template(
            "form.html", fields=fields, table="personal_data"
        )
    if request.method == "POST":
        values_for_passportdata = list()
        values_for_personaldata = list()
        keys = list(request.form.keys())
        column_for_personaldata = keys[:-3:]
        column_for_personaldata.append(keys[-1])
        column_for_passportdata = [keys[4]]
        column_for_passportdata.extend(keys[-3:-1:])
        column_for_personaldata = ", ".join(column_for_personaldata)
        column_for_passportdata = ", ".join(column_for_passportdata)

        for key in keys:
            if key == "passportdate" or key == "region":
                values_for_passportdata.append(request.form[key])
            elif key == "age" or key == "passport" or key == "payment":
                if key == "passport":
                    values_for_passportdata.append(int(request.form[key]))
                values_for_personaldata.append(int(request.form[key]))
            else:
                values_for_personaldata.append(request.form[key])
        # Вставка данных в таблицу, функция импортированная из другого файла
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
        return redirect(url_for("personaldata"))


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
