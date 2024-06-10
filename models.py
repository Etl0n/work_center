from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PassportData(db.Model):
    __table_args__ = {'schema': 'centre_work'}
    id = db.Column(db.Integer, primary_key=True)
    passport = db.Column(db.Integer, nullable=True, unique=True)
    passportdate = db.Column(db.Date, nullable=True)
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
    person = db.relationship('Regperson', back_populates='vacancy')


class Regperson(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('id', 'idreg', name='composite_pk'),
        {'schema': 'centre_work'},
    )
    id = db.Column(
        db.Integer,
        db.ForeignKey('centre_work.personal_data.joblessid'),
    )
    idreg = db.Column(db.Integer)
    registrar = db.Column(db.String(100), nullable=True)
    regdate = db.Column(db.Date, nullable=True, default=datetime.now())
    archivist = db.Column(db.String(100), nullable=False)
    archivesdate = db.Column(
        db.Date, nullable=True, default=datetime(year=9999, month=12, day=31)
    )
    active = db.Column(db.Boolean, nullable=True, default=True)
    vacancy = db.Column(db.Integer, db.ForeignKey('centre_work.vacancy.jobid'))
