from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from app import db


class User(UserMixin):
    type_id = []
    type = -1

    __tablename__ = 'User'
    _id = db.Column(db.Integer, primary_key=True)
    passwd_hash = db.Column(db.String(128),nullable=False)
    name = db.Column(db.String(64),nullable=False)
    id = db.Column(db.Integer,unique=True,nullable=False)   
    permission = db.Column(db.Integer,default=0,nullable=False)
    sex = db.Column(db.Boolean)

    def query_user(type_id):
        try:
            if isinstance(type_id,str):
                type_id = eval(type_id)

            if not isinstance(type_id,list) or len(type_id)!=2:
                result = None
            if int(type_id[0]) == 0:
                result =  Student.query.filter_by(id=int(type_id[1])).first()
            if int(type_id[0]) == 1:
                result = Teacher.query.filter_by(id=int(type_id[1])).first()
            if int(type_id[0]) == 2:
                result = Admin.query.filter_by(id=int(type_id[1])).first()
            if result != None :
                result.type_id = type_id
                result.type = type_id[0]
        except Exception as e:
            print(e)
            return None
            
        return result

    def get_id(self):
        return str(self.type_id)

    @property
    def passwd(self):
        raise AttributeError('password is not a readable attribute')

    @passwd.setter
    def passwd(self, passwd):
        self.passwd_hash = generate_password_hash(passwd)

    def verify_passwd(self, passwd):
        return check_password_hash(self.passwd_hash, passwd)

    def __repr__(self):
        return '<{} ： {}>'.format(self.__tablename__,self.name)

class Student(User,db.Model):
    __tablename__ = 'student'


    _class = db.Column(db.String(64))
    courses = db.relationship("Course_Teach_Stu",backref='student')
    

class Teacher(User,db.Model):
    __tablename__ = 'teacher'

    courses = db.relationship("Course_Teach_Stu",backref='teacher')


class Admin(User,db.Model):
    __tablename__ = 'admin'

    
class Course(db.Model):
    __tablename__ = 'course'
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(64),unique=True,nullable=False)
    name = db.Column(db.String(64),nullable=False)
    college = db.Column(db.String(64),nullable=False)
    courses = db.relationship("Course_Teach_Stu",backref='cour')

class Course_Teach_Stu(db.Model):
    __tablename__ = 'course_teach_stu'
    _id = db.Column(db.Integer, primary_key=True)
    stu = db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    teach = db.Column(db.Integer,db.ForeignKey('teacher.id'),nullable=False)
    course = db.Column(db.String(64),db.ForeignKey('course.id'),nullable=False)
    source = db.Column(db.Integer,nullable=True)
    
@login_manager.user_loader
def load_user(type_id):
    return User.query_user(type_id)