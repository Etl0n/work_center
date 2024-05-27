from get_data import get_content, insert_data
from flask import Flask, render_template, redirect, url_for
from flask import request
import psycopg2 as ps

app = Flask(__name__)

LIST_DATABASE=['personaldata','education','passportdata', 'regperson', 'vacancy', 'the_worst_vacancy', 'free_vacancy', 'the_best_salary']

DATABASE = {
    'host': 'localhost',
    'port': 5432,
    'database': 'cw',
    'user': 'postgres',
    'password': 'BdktdF2004',
}


#Подключение к БД
try:
    conn = ps.connect(**DATABASE)
    print(f'Вы подключены к базе данных "cw" как пользователь "postgres".')
except ps.OperationalError as e:       
    print('Can`t establish connection to  databse')
    raise


@app.route('/')
def index():
    return render_template('menu.html', name_database='Главаное меню', list_database=LIST_DATABASE)


@app.route('/personaldata/', methods = ['GET'])
def personaldata():
    if request.method=='GET':
        data=[]
        data.append(tuple(['joblessid','lastname','firstname','patronymic','age', 'passport', 'address','phone', 'picture', 'payment','experience']))
        data+=get_content(conn=conn, database='personaldata')
        return render_template('personaldata.html', data=data)

@app.route('/education/')
def education():
    if request.method=='GET':
        data=[]
        data.append(tuple(['id','joblessid','studyplace','studyaddress','studytype']))
        data+=get_content(conn=conn, database='education')
        return render_template('viewlist.html', data=data, add_form=False)

@app.route('/passportdata/')
def passportdata():
    if request.method=='GET':
        data=[]
        data.append(tuple(['passport','passportdate','region']))
        data+=get_content(conn=conn, database='passportdata')
        return render_template('viewlist.html', data=data, add_form=False)

@app.route('/regperson/')
def regperson():
    if request.method=='GET':
        data=[]
        data.append(tuple(['id','idreg','registrar','regdate','arhivist','archivesdate','active','vacancy']))
        data+=get_content(conn=conn, database='regperson')
        return render_template('viewlist.html', data=data, add_form=True)

@app.route('/vacancy/')
def vacancy():
    if request.method=='GET':
        data=[]
        data.append(tuple(['jobid','jobtype', 'jobname','jobgiver','place','mobile','district','money','more','active']))
        data+=get_content(conn=conn, database='vacancy')
        return render_template('viewlist.html', data=data, add_form=True)
    
#первый доп запрос
@app.route('/the_worst_vacancy/', methods=['GET'])
def the_worst_vacancy():
    cursor= conn.cursor()
    data=[]
    data.append(tuple(['jobname', 'count']))
    cursor.execute('with cte as (SELECT v.jobname, COUNT(*) as count ' \
                    'FROM centre_work.regperson as r ' \
                    'JOIN centre_work.vacancy as v ON r.vacancy=v.jobid '\
                    'GROUP BY v.jobname) '\
                    'SELECT v.jobname, cte.count '\
                    'FROM centre_work.vacancy as v '\
                    'JOIN cte ON v.jobname=cte.jobname '\
                    'WHERE cte.count=(SELECT MAX(cte.count) '\
                    'FROM cte)')
    data.extend(cursor.fetchall())
    cursor.close()
    return render_template('viewlist.html', data=data, add_form=False)

#второй доп запрос
@app.route('/free_vacancy/', methods=['GET'])
def free_vacancy():
    cursor= conn.cursor()
    data=[]
    data.append(tuple(['jobid','jobtype', 'jobname','jobgiver','place','mobile','district','money','more','active']))
    cursor.execute('SELECT * FROM centre_work.vacancy WHERE active=True')
    data.extend(cursor.fetchall())
    cursor.close()
    return render_template('viewlist.html', data=data, add_form=False)

#третий доп запрос
@app.route('/the_best_salary/', methods=['GET'])
def the_best_salary():
    cursor= conn.cursor()
    data=[]
    data.append(tuple(['jobid','jobtype', 'jobname','jobgiver','place','mobile','district','money','more','active']))
    cursor.execute('SELECT * FROM centre_work.vacancy as v WHERE v.money=(SELECT MAX(v.money) FROM centre_work.vacancy as v)')
    data.extend(cursor.fetchall())
    cursor.close()
    return render_template('viewlist.html', data=data, add_form=False)
    

@app.route('/personaldata/form/', methods=['POST', 'GET'])
def add_personal():
    if request.method=='GET':
        fields = {
            'Имя': 'firstname',
            'Фамилия': 'lastname',
            'Отчество': 'patronymic',
            'Возраст': 'age',
            'Номер паспора': 'passport',
            'Адресс': 'address',
            'Номер телефона': 'phone',
            'Ссылка на фотографию': 'picture',
            'Желаемая зарплата': 'payment',
            'Дата регистрации паспорта': 'passportdate',
            'Место регитрации паспорта': 'region',
        }
        return render_template('form.html', fields=fields, table='personaldata')
    if request.method=='POST':
        values_for_passportdata=list()
        values_for_personaldata=list()
        keys=list(request.form.keys())
        column_for_personaldata=keys[:-3:]
        column_for_personaldata.append(keys[-1])
        column_for_passportdata=[keys[4]]
        column_for_passportdata.extend(keys[-3:-1:])
        column_for_personaldata=", ".join(column_for_personaldata)
        column_for_passportdata=", ".join(column_for_passportdata)


        for key in keys:
            if key=='passportdate' or key=='region':
                values_for_passportdata.append(request.form[key])
            elif key=='age' or key=='passport' or key=='payment': 
                if key=='passport':
                    values_for_passportdata.append(int(request.form[key]))
                values_for_personaldata.append(int(request.form[key]))
            else:
                values_for_personaldata.append(request.form[key])

        insert_data(conn=conn, database='passportdata', column=column_for_passportdata, values=values_for_passportdata)
        insert_data(conn=conn, database='personaldata', column=column_for_personaldata, values=values_for_personaldata)
        return redirect(url_for('personaldata'))

@app.route('/vacancy/form/', methods=['POST', 'GET'])
def add_vacancy():
    if request.method=='GET':
        fields = {
            'Тип вакансии': 'jobtype',
            'Название вакансии': 'jobname',
            'Работадель': 'jobgiver',
            'Адрес работадателя': 'place',
            'Телефон работадателя': 'mobile',
            'Район в котором предоставляется работа': 'district',
            'Зарплата': 'money',
            'Доп информация': 'more',
        }
        return render_template('form.html', fields=fields, table='vacancy')
    
    if request.method=='POST':
        keys=list(request.form.keys())
        column=", ".join(keys)
        values=[request.form[x] for x in keys]
        insert_data(conn=conn, database='vacancy', column=column, values=values)
        return redirect(url_for('vacancy'))
    

@app.route('/regperson/form/', methods=['POST', 'GET'])
def add_regperson():
    if request.method=='GET':
        fields = {
            'ID пользователя': 'id',
            'Фамилия регистрирующего': 'registrar',
            'Дата постановки на учет': 'regdate',
            'Фамилия добавившего в архив': 'archivist',
            'Дата добавления в архив': 'archivesdate',
            'Вакансия' : 'vacancy'
        }
        return render_template('form.html', fields=fields, table='regperson')
    
    if request.method=='POST':
        keys=list(request.form.keys())
        values=[request.form[x] for x in keys]
        keys.append('idreg')
        column=", ".join(keys)
        insert_data(conn=conn, database='regperson', column=column, values=values)
        return redirect(url_for('regperson'))



if __name__=='__main__':
    app.run('127.0.0.1', port='8000')