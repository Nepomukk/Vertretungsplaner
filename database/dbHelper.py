from sqlalchemy import Column, create_engine, Date, Identity, text
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import psycopg2, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    userid = Column(Integer, nullable=False, primary_key=True)
    username = Column(String, nullable=False)
    pwd = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __init__(self, username, pwd, firstname, lastname, email):
        self.username = username
        self.pwd = pwd
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def __repr__(self):
        return f"User(userid={self.userid!r}, " \
               f"username={self.username!r}, " \
               f"firstname={self.firstname!r}, " \
               f"lastname={self.lastname!r}, " \
               f"pwd={self.pwd!r}, " \
               f"email={self.email!r})"


class AbsenseReasons(Base):
    __tablename__ = "absensereasons"

    id = Column(Integer, nullable=False, primary_key=True)
    descr = Column(String, nullable=False)

    def __init__(self, descr):
        self.descr = descr

    def __repr__(self):
        return f"AbsenceReasons(id={self.id!r}, " \
               f"descr={self.descr!r})"


class StatusTypes(Base):
    __tablename__ = "statustypes"

    id = Column(Integer, nullable=False, primary_key=True)
    descr = Column(String, nullable=False)

    def __init__(self, descr):
        self.descr = descr

    def __repr__(self):
        return f"StatusTypes(id={self.id!r}, " \
               f"descr={self.descr!r})"


class SubstitutionTypes(Base):
    __tablename__ = "substitutiontypes"

    id = Column(Integer, nullable=False, primary_key=True)
    descr = Column(String, nullable=False)

    def __init__(self, descr):
        self.descr = descr

    def __repr__(self):
        return f"SubstitutionTypes(id={self.id!r}, " \
               f"descr={self.descr!r})"


class Departments(Base):
    __tablename__ = "departments"

    id = Column(Integer, nullable=False, primary_key=True)
    descr = Column(String, nullable=False)
    shortcut = Column(String, nullable=False)

    def __init__(self, descr, shortcut):
        self.descr = descr
        self.shortcut = shortcut

    def __repr__(self):
        return f"Departments(id={self.id!r}, " \
               f"descr={self.descr!r}, " \
               f"shortcut={self.shortcut!r})"


class UserToRole(Base):
    __tablename__ = "usertorole"

    userid = Column(Integer, ForeignKey("users.userid"), nullable=False, primary_key=True)
    roleid = Column(Integer, ForeignKey("roles.roleid"), nullable=False, primary_key=True)
    departmentid = Column(Integer, ForeignKey("departments.id"), nullable=False, primary_key=True)

    def __init__(self, userid, roleid, departmentid):
        self.userid = userid
        self.roleid = roleid
        self.departmentid = departmentid

    def __repr__(self):
        return f"UserToRole(userid={self.userid!r}, " \
               f"roleid={self.roleid!r}, " \
               f"departmentid={self.departmentid!r})"


class FormaToDepartment(Base):
    __tablename__ = "fromattodepartment"

    roleid = Column(Integer, ForeignKey("roles.roleid"), nullable=False, primary_key=True)
    departmentid = Column(Integer, ForeignKey("departments.id"), nullable=False, primary_key=True)

    def __init__(self, roleid, departmentid):
        self.roleid = roleid
        self.departmentid = departmentid

    def __repr__(self):
        return f"FormaToDepartment(roleid={self.roleid!r}, " \
               f"departmentid={self.departmentid!r})"


class SubLessons(Base):
    __tablename__ = "sublessons"

    posid = Column(Integer, nullable=False, primary_key=True)
    formatid = Column(Integer, ForeignKey("forms.formatid"), nullable=False)
    lessonnumber = Column(Integer, nullable=False)
    lessontype = Column(String, nullable=False)
    classname = Column(String, nullable=False)
    subteachingtype = Column(Integer, ForeignKey("substitutiontypes.id"), nullable=False)
    subteacher = Column(Integer, ForeignKey("users.userid"), nullable=False)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    createdate = Column(Date, nullable=False)

    def __init__(self, formatid, lessonnumber, lessontype, classname, subteachingtype, subteacher, userid,
                 createdate):
        self.formatid = formatid
        self.lessonnumber = lessonnumber
        self.lessontype = lessontype
        self.classname = classname
        self.subteachingtype = subteachingtype
        self.subteacher = subteacher
        self.userid = userid
        self.createdate = createdate

    def __repr__(self):
        return f"SubLessons(posid={self.posid!r}, " \
               f"formatid={self.formatid!r}" \
               f"lessonnumber={self.lessonnumber!r}" \
               f"lessontype={self.lessontype!r}" \
               f"classname={self.classname!r}" \
               f"subteachingtype={self.subteachingtype!r}" \
               f"subteacher={self.subteacher!r}" \
               f"userid={self.userid!r}" \
               f"createdate={self.createdate!r})"


class Forms(Base):
    __tablename__ = "forms"

    formatid = Column(Integer, nullable=False, primary_key=True)
    absensereasons = Column(Integer, ForeignKey("absensereasons.id"), nullable=False)
    other = Column(String)
    appendfile = Column(String)
    workarea = Column(String)
    pdffile = Column(String)
    status = Column(Integer, ForeignKey("statustypes.id"), nullable=False)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    createdate = Column(Date, nullable=False)
    activ = Column(Boolean, nullable=False)
    fcomment = Column(String)

    def __init__(self, userid, absensereasons, other, appendfile, workarea, pdffile, status, fcomment, activ,
                 createdate):
        self.absensereasons = absensereasons
        self.other = other
        self.appendfile = appendfile
        self.workarea = workarea
        self.pdffile = pdffile
        self.status = status
        self.userid = userid
        self.createdate = createdate
        self.activ = activ
        self.fcomment = fcomment

    def __repr__(self):
        return f"Forms(formatid={self.formatid!r}, " \
               f"absensereasons={self.absensereasons!r}, " \
               f"other={self.other!r}, " \
               f"appendfile={self.appendfile!r}, " \
               f"workarea={self.workarea!r}, " \
               f"pdffile={self.pdffile!r}, " \
               f"status={self.status!r}, " \
               f"userid={self.userid!r}, " \
               f"createdate={self.createdate!r}, " \
               f"activ={self.activ!r}, " \
               f"fcomment={self.fcomment!r})"


class Confirmation(Base):
    __tablename__ = "confirmation"

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    formatid = Column(Integer, ForeignKey("forms.formatid"), nullable=False)
    comdate = Column(TIMESTAMP, nullable=False)
    ok = Column(Boolean, nullable=False)

    def __init__(self, userid, formatid, comdate, ok):
        self.userid = userid
        self.formatid = formatid
        self.comdate = comdate
        self.ok = ok

    def __repr__(self):
        return f"Forms(id={self.id!r}, " \
               f"userid={self.userid!r}, " \
               f"formatid={self.formatid!r}, " \
               f"comdate={self.comdate!r}, " \
               f"ok={self.ok!r})"


# Example
# we can now construct a Session() without needing to pass the
# engine each time
# with Session() as session:
#     session.add(some_object)
#     session.add(some_other_object)
#     session.commit()
class Session:

    @staticmethod
    def getSession():
        engine = create_engine("postgresql+psycopg2://postgres:docker@localhost:5432/postgres")
        Session = sessionmaker(bind=engine)
        return Session

    @staticmethod
    def createDatabase():
        engine = create_engine("postgresql+psycopg2://postgres:docker@localhost:5432/postgres")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(Departments('AV Abteilung', 'AV'))
            session.add(Departments('Elektrotechnik', 'ET'))
            session.add(Departments('IT Abteilung', 'IT'))
            session.add(Departments('BFS Abteilung', 'BFS'))
            session.add(Departments('ITA Abteilung', 'ITA'))
            session.add(Departments('FOS Abteilung', 'FOS'))
            session.add(Departments('FS Abteilung', 'FS'))

            session.add(AbsenseReasons('Dienstveranstaltung'))
            session.add(AbsenseReasons('Prüfungsausschuss'))
            session.add(AbsenseReasons('Fortbildung'))
            session.add(AbsenseReasons('Unterrichtsgang'))
            session.add(AbsenseReasons('Sonstiges'))

            session.add(SubstitutionTypes('Fachvertretung'))
            session.add(SubstitutionTypes('passive Vertretung'))

            session.add(StatusTypes('erstellt'))
            session.add(StatusTypes('bearbeiten fertig gestellt'))
            session.add(StatusTypes('abgelehnt von Bereichsleiter'))
            session.add(StatusTypes('angenommen von Bereichsleiter'))
            session.add(StatusTypes('abgelehnt von Vertretungsplaner'))
            session.add(StatusTypes('angenommen von Vertretungsplaner'))

            session.commit()

    @staticmethod
    def dropDatabase():
        engine = create_engine("postgresql+psycopg2://postgres:docker@localhost:5432/postgres")
        Base.metadata.drop_all(engine)


if __name__ == '__main__':
    Session.createDatabase()