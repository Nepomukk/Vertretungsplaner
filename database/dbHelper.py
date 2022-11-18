from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    userid = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    pwd = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.userid

    def __init__(self, username, pwd, firstname, lastname, email):
        self.username = username
        self.pwd = generate_password_hash(pwd)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def __repr__(self):
        return f"<User userid={self.userid!r}, " \
               f"username={self.username!r}, " \
               f"firstname={self.firstname!r}, " \
               f"lastname={self.lastname!r}, " \
               f"pwd={self.pwd!r}, " \
               f"email={self.email!r}>"


class AbsenseReasons(db.Model):
    __tablename__ = "absensereasons"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    descr = db.Column(db.String, nullable=False)

    def __init__(self, descr):
        self.descr = descr

    def __repr__(self):
        return f"<AbsenceReasons id={self.id!r}, " \
               f"descr={self.descr!r}>"


class StatusTypes(db.Model):
    __tablename__ = "statustypes"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    descr = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    def __init__(self, descr, color):
        self.descr = descr
        self.color = color

    def __repr__(self):
        return f"<StatusTypes id={self.id!r}, " \
               f"descr={self.descr!r}, " \
               f"color={self.color!r}>"


class SubstitutionTypes(db.Model):
    __tablename__ = "substitutiontypes"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    descr = db.Column(db.String, nullable=False)

    def __init__(self, descr):
        self.descr = descr

    def __repr__(self):
        return f"<SubstitutionTypes id={self.id!r}, " \
               f"descr={self.descr!r}>"


class Roles(db.Model):
    __tablename__ = "roles"

    roleid = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    level = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, name, admin, level):
        self.name = name
        self.admin = admin
        self.level = level

    def __repr__(self):
        return f"<Roles roleid={self.roleid!r}, " \
               f"name={self.name!r}, " \
               f"admin={self.admin!r}, " \
               f"level={self.level!r}>"

#
fromattodepartment = db.Table('fromattodepartment',
                            db.Column('formatid', db.Integer, ForeignKey("forms.formatid"), nullable=False,
                                      primary_key=True),
                            db.Column('departmentid', db.Integer, ForeignKey("departments.id"), nullable=False,
                                      primary_key=True))

class FromatToDepartment(db.Model):
    __tablename__ = "fromattodepartment"
    __table_args__ = {'extend_existing': True}

    formatid = db.Column('formatid', db.Integer, ForeignKey("forms.formatid"), nullable=False, primary_key=True)
    departmentid = db.Column('departmentid', db.Integer, ForeignKey("departments.id"), nullable=False, primary_key=True)

    def __init__(self, formatid, departmentid):
        self.formatid = formatid
        self.departmentid = departmentid

    def __repr__(self):
        return f"<FromatToDepartment formatid={self.formatid!r}, " \
               f"departmentid={self.departmentid!r}, " \
               f"department={self.department!r}>"


class Departments(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    descr = db.Column(db.String, nullable=False)
    shortcut = db.Column(db.String, nullable=False)

    def __init__(self, descr, shortcut):
        self.descr = descr
        self.shortcut = shortcut

    def __repr__(self):
        return f"<Departments id={self.id!r}, " \
               f"descr={self.descr!r}, " \
               f"shortcut={self.shortcut!r}>"


class UserToRole(db.Model):
    __tablename__ = "usertorole"

    userid = db.Column(db.Integer, ForeignKey("users.userid"), nullable=False, primary_key=True)
    roleid = db.Column(db.Integer, ForeignKey("roles.roleid"), nullable=False, primary_key=True)
    departmentid = db.Column(db.Integer, ForeignKey("departments.id"), nullable=False, primary_key=True)

    def __init__(self, userid, roleid, departmentid):
        self.userid = userid
        self.roleid = roleid
        self.departmentid = departmentid

    def __repr__(self):
        return f"<UserToRole userid={self.userid!r}, " \
               f"roleid={self.roleid!r}, " \
               f"departmentid={self.departmentid!r}>"


class SubLessons(db.Model):
    __tablename__ = "sublessons"

    posid = db.Column(db.Integer, nullable=False, primary_key=True)
    formatid = db.Column(db.Integer, ForeignKey("forms.formatid"), nullable=False)
    lessonnumberfrom = db.Column(db.Integer, nullable=False)
    lessonnumberto = db.Column(db.Integer, nullable=False)
    lessontype = db.Column(db.String, nullable=False)
    lessondate = db.Column(db.Date, nullable=False)
    classname = db.Column(db.String, nullable=False)
    subteachingtype = db.Column(db.Integer, ForeignKey("substitutiontypes.id"))
    subcontend = db.Column(db.String)
    subteacher = db.Column(db.Integer, ForeignKey("users.userid"), nullable=False)
    userid = db.Column(db.Integer, ForeignKey("users.userid"), nullable=False)
    createdate = db.Column(db.Date, nullable=False)
    user = db.relationship('User', foreign_keys='SubLessons.userid')
    teacher = db.relationship('User', foreign_keys='SubLessons.subteacher')
    subtype = db.relationship('SubstitutionTypes')

    def __init__(self, formatid, lessonnumberfrom, lessonnumberto, lessontype, classname, subteachingtype, subteacher,
                 userid,
                 createdate, subcontend, lessondate):
        self.formatid = formatid
        self.lessonnumberfrom = lessonnumberfrom
        self.lessontype = lessontype
        self.classname = classname
        self.subteachingtype = subteachingtype
        self.subteacher = subteacher
        self.userid = userid
        self.createdate = createdate
        self.lessonnumberto = lessonnumberto
        self.subcontend = subcontend
        self.lessondate = lessondate

    def __repr__(self):
        return f"<SubLessons posid={self.posid!r}, " \
               f"formatid={self.formatid!r}, " \
               f"lessonnumberfrom={self.lessonnumberfrom!r}, " \
               f"lessontype={self.lessontype!r}, " \
               f"classname={self.classname!r}, " \
               f"subteachingtype={self.subteachingtype!r}, " \
               f"subteacher={self.subteacher!r}, " \
               f"userid={self.userid!r}, " \
               f"lessonnumberto={self.lessonnumberto!r}, " \
               f"subcontend={self.subcontend!r}, " \
               f"lessondate={self.lessondate!r}, " \
               f"createdate={self.createdate!r}, " \
               f"user={self.user!r}, " \
               f"teacher={self.teacher!r}, " \
               f"subtype={self.subtype!r}>"


class Forms(db.Model):
    __tablename__ = "forms"

    formatid = db.Column(db.Integer, nullable=False, primary_key=True)
    absensereasons = db.Column(db.Integer, ForeignKey("absensereasons.id"), nullable=False)
    other = db.Column(db.String)
    appendfile = db.Column(db.String)
    workarea = db.Column(db.Integer)
    pdffile = db.Column(db.String)
    status = db.Column(db.Integer, ForeignKey("statustypes.id"), nullable=False)
    userid = db.Column(db.Integer, ForeignKey("users.userid"), nullable=False)
    createdate = db.Column(db.Date, nullable=False)
    activ = db.Column(db.Boolean, nullable=False)
    fcomment = db.Column(db.String)
    absense = db.relationship('AbsenseReasons')
    statusrel = db.relationship('StatusTypes')
    user = db.relationship('User')
    departments = db.relationship('Departments', secondary=fromattodepartment)
    sublessons = db.relationship("SubLessons", order_by="SubLessons.lessondate")

    def __init__(self, userid, absensereasons, other, workarea, status, fcomment, activ,
                 createdate):
        self.absensereasons = absensereasons
        self.other = other
        self.workarea = workarea
        self.status = status
        self.userid = userid
        self.createdate = createdate
        self.activ = activ
        self.fcomment = fcomment
        self.pdffile = None
        self.appendfile = None

    def __repr__(self):
        return f"<Forms formatid={self.formatid!r}, " \
               f"absensereasons={self.absensereasons!r}, " \
               f"other={self.other!r}, " \
               f"appendfile={self.appendfile!r}, " \
               f"workarea={self.workarea!r}, " \
               f"pdffile={self.pdffile!r}, " \
               f"status={self.status!r}, " \
               f"userid={self.userid!r}, " \
               f"createdate={self.createdate!r}, " \
               f"activ={self.activ!r}, " \
               f"fcomment={self.fcomment!r}, " \
               f"user={self.user!r}, " \
               f"statusrel={self.statusrel!r}, " \
               f"departments={self.departments!r}, " \
               f"sublessons={self.sublessons!r}, " \
               f"absense={self.absense!r}>"


class Confirmation(db.Model):
    __tablename__ = "confirmation"

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, ForeignKey("users.userid"), nullable=False)
    formatid = db.Column(db.Integer, ForeignKey("forms.formatid"), nullable=False)
    comdate = db.Column(db.TIMESTAMP, nullable=False)
    ok = db.Column(db.Boolean, nullable=False)

    def __init__(self, userid, formatid, comdate, ok):
        self.userid = userid
        self.formatid = formatid
        self.comdate = comdate
        self.ok = ok

    def __repr__(self):
        return f"<Forms id={self.id!r}, " \
               f"userid={self.userid!r}, " \
               f"formatid={self.formatid!r}, " \
               f"comdate={self.comdate!r}, " \
               f"ok={self.ok!r}>"
