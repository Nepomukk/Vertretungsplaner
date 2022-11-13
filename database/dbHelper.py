from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import BINARY
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"User(userid={self.userid!r}, " \
               f"username={self.username!r}, " \
               f"password={self.password!r}, " \
               f"email={self.email!r})"


class AbsenceReasons(Base):
    __tablename__ = "absencereasons"

    id = Column(Integer, primary_key=True)
    descr = Column(String)

    def __repr__(self):
        return f"AbsenceReasons(id={self.id!r}, " \
               f"descr={self.descr!r})"


class StatusTypes(Base):
    __tablename__ = "statustypes"

    id = Column(Integer, primary_key=True)
    descr = Column(String)

    def __repr__(self):
        return f"StatusTypes(id={self.id!r}, " \
               f"descr={self.descr!r})"


class SubstitutionTypes(Base):
    __tablename__ = "substitutiontypes"

    id = Column(Integer, primary_key=True)
    descr = Column(String)

    def __repr__(self):
        return f"SubstitutionTypes(id={self.id!r}, " \
               f"descr={self.descr!r})"


class Roles(Base):
    __tablename__ = "roles"

    roleid = Column(Integer, primary_key=True)
    role = Column(String)

    def __repr__(self):
        return f"Roles(roleid={self.roleid!r}, " \
               f"role={self.role!r})"


class Departments(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    descr = Column(String)
    additionalinfo = Column(String)

    def __repr__(self):
        return f"Departments(id={self.id!r}, " \
               f"descr={self.descr!r}, " \
               f"additionalinfo={self.additionalinfo!r})"


class Usertorole(Base):
    __tablename__ = "usertorole"

    userid = Column(Integer, ForeignKey("users.userid"))
    roleid = Column(Integer, ForeignKey("roles.roleid"))

    def __repr__(self):
        return f"Usertorole(userid={self.userid!r}, " \
               f"roleid={self.roleid!r})"


class SubLessons(Base):
    __tablename__ = "sublessons"

    posid = Column(Integer, primary_key=True)
    formatid = Column(Integer, ForeignKey("forms.formatid"))
    lessonnumber = Column(Integer)
    lessontype = Column(String)
    classname = Column(String)
    subteachingtype = Column(Integer, ForeignKey("substitutiontypes.id"))
    subteacher = Column(String)
    lastuser = Column(Integer, nullable=False)
    lastchange = Column(Integer, nullable=False)

    def __repr__(self):
        return f"SubLessons(posid={self.posid!r}, " \
               f"formatid={self.formatid!r}" \
               f"lessonnumber={self.lessonnumber!r}" \
               f"lessontype={self.lessontype!r}" \
               f"classname={self.classname!r}" \
               f"subteachingtype={self.subteachingtype!r}" \
               f"subteacher={self.subteacher!r}" \
               f"lastuser={self.lastuser!r}" \
               f"lastchange={self.lastchange!r})"


class Forms(Base):
    __tablename__ = "forms"

    formatid = Column(Integer, primary_key=True)
    userid = Column(Integer)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    absensetype = Column(Integer, ForeignKey("absencereasons.id"))
    other = Column(String)
    appendfile = Column(BINARY)
    workarea = Column(String)
    pdffile = Column(BINARY)
    status = Column(Integer, ForeignKey("statustypes.id"), nullable=False)
    comment = Column(String)
    lastuser = Column(Integer, nullable=False)
    lastchange = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Forms(formatid={self.formatid!r}, " \
               f"userid={self.userid!r}, " \
               f"firstname={self.firstname!r}, " \
               f"lastname={self.lastname!r}, " \
               f"absensetype={self.absensetype!r}, " \
               f"other={self.other!r}, " \
               f"appendfile={self.appendfile!r}, " \
               f"workarea={self.workarea!r}, " \
               f"pdffile={self.pdffile!r}, " \
               f"status={self.status!r}, " \
               f"comment={self.comment!r}, " \
               f"lastuser={self.lastuser!r}, " \
               f"lastchange={self.lastchange!r})"
