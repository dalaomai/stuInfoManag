from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from app import db
from config import RolePermission
from sqlalchemy import and_

from app.decorators import permission_required
from config import Permission


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
        if(len(passwd)<6):
            raise Exception('密码修改失败')
            return 0
        self.passwd_hash = generate_password_hash(passwd)

    def verify_passwd(self, passwd):
        return check_password_hash(self.passwd_hash, passwd)

    def can(self,permission):
        return (self.permission&permission)==permission

    def __repr__(self):
        return '<{} ： {}>'.format(self.__tablename__,self.name)

    @permission_required(Permission.PERSONAL_INFO)
    def modifyBaseInfo(self,passwd=None):
        if passwd:
            self.passwd = passwd
        db.session.add(self)
        return db.session.commit()

    @permission_required(RolePermission.ADMIN)
    def getAllCourse(self):
        result = db.session.query(Course)
        return result

    @permission_required(RolePermission.ADMIN)
    def getAllStudent(self):
        result = db.session.query(Student,_class).filter(Student._class==_class._id)
        return result

    @permission_required(RolePermission.ADMIN)
    def getAllTeacher(self):
        result = db.session.query(Teacher)
        return result

    @permission_required(RolePermission.ADMIN)
    def getAllClass(self):
        result = db.session.query(_class)
        return result


    @permission_required(RolePermission.ROOT)
    def getAllAdmin(self):
        result = db.session.query(Admin)
        return result

    def getCoursesInfo(self):
        return db.session.query(Student,Teacher,Course,Course_Teach_Stu,_class).filter(and_(Student.id == Course_Teach_Stu.stu,Teacher.id == Course_Teach_Stu.teach,Course.id==Course_Teach_Stu.course,_class._id==Student._class))
        
class Student(User,db.Model):
    __tablename__ = 'student'

    permission = db.Column(db.Integer,default=RolePermission.STUDENT,nullable=False)
    _class = db.Column(db.Integer,db.ForeignKey('_class._id'),default=0,nullable=False)
    courses = db.relationship("Course_Teach_Stu",backref='student')

    @permission_required(RolePermission.STUDENT)
    def modifyBaseInfo(self,passwd=None):
        if passwd:
            self.passwd = passwd
        db.session.add(self)
        return db.session.commit()

    @permission_required(RolePermission.STUDENT)
    def getCoursesInfo(self):
        result = super().getCoursesInfo().filter(Student.id==self.id)
        return result
    
class Teacher(User,db.Model):
    __tablename__ = 'teacher'
    permission = db.Column(db.Integer,default=RolePermission.TEACHER,nullable=False)
    courses = db.relationship("Course_Teach_Stu",backref='teacher')

    @permission_required(RolePermission.TEACHER)
    def modifyBaseInfo(self,passwd=None):
        if passwd:
            self.passwd = passwd
        db.session.add(self)
        return db.session.commit()

    @permission_required(RolePermission.TEACHER)
    def getCoursesInfo(self):
        result = super().getCoursesInfo().filter(Teacher.id==self.id)
        return result

class Admin(User,db.Model):
    permission = db.Column(db.Integer,default=RolePermission.ADMIN,nullable=False)
    __tablename__ = 'admin'

    @permission_required(RolePermission.ADMIN)
    def modifyBaseInfo(self,passwd=None):
        if passwd:
            self.passwd = passwd
        db.session.add(self)
        return db.session.commit()

    @permission_required(RolePermission.ADMIN)
    def getCoursesInfo(self):
        result = super().getCoursesInfo()
        return result

class Course(db.Model):
    __tablename__ = 'course'
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(64),unique=True,nullable=False)
    name = db.Column(db.String(64),nullable=False)
    college = db.Column(db.String(64),nullable=False)
    courses = db.relationship("Course_Teach_Stu",backref='cour')

class _class(db.Model):
    __tablename__ = '_class'
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False,unique=True)
    students = db.relationship("Student",backref='aclass')
            
class Course_Teach_Stu(db.Model):
    __tablename__ = 'course_teach_stu'
    _id = db.Column(db.Integer, primary_key=True)
    stu = db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    teach = db.Column(db.Integer,db.ForeignKey('teacher.id'),nullable=False)
    course = db.Column(db.String(64),db.ForeignKey('course.id'),nullable=False)
    source = db.Column(db.Integer,nullable=True)
    semester = db.Column(db.String(64),nullable=False)
    
@login_manager.user_loader
def load_user(type_id):
    return User.query_user(type_id)