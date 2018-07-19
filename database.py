from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
 
engine = create_engine('sqlite:///resume.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, nullable = True)
    username = Column(String, unique = True)
    password = Column(String)
    email = Column(String)
    access = Column(Integer)
 
    #--------------------------------------------------------------------
    def __init__(self, id, username, password, email, access):
        """"""
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.access = access
 
##########################################################################
class Resume(Base):
    """"""
    __tablename__ = "resumes"
 
    id = Column(Integer, primary_key=True, nullable = True)
    uid = Column(Integer, ForeignKey(User.id))
    user = relationship ('User')
    firstname = Column(String)
    lastname = Column(String)
    education = Column(String)
    picture = Column(Text)
    document = Column(Text)
    skill = Column(String)
 
    #----------------------------------------------------------------------
    def __init__(self, id, uid, firstname, lastname, education, picture, document, skill):
        """"""
        self.id = id
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.education = education
        self.picture = picture
        self.document = document
        self.skill = skill

############################################################################
class Comment(Base):
    """"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key = True, nullable = True)
    uid = Column(String, ForeignKey(User.id))
    user = relationship('User')
    rid = Column(String, ForeignKey(Resume.id))
    resume = relationship('Resume')
    content = Column(Text)

    #----------------------------------------------------------------------
    def __init__(self, id, uid, rid, content):
        """"""
        self.id = id
        self.uid = uid
        self.rid = rid
        self.content = content

# create tables
Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()

# admin_user = User(1, 'administrator', 'admin', 'admin@admin.com', 1)
# teacher_user = User(2, 'teacher', 'teacher', 'teacher@teacher.com', 2)

# session.add(admin_user)
# session.add(teacher_user)
# session.commit()