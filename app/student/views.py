from . import student

from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,current_user,login_required,logout_user
from config import Config
from app.decorators import permission_required
from config import Permission,RolePermission
import json
from sqlalchemy import desc,asc
from app.models import Student,Teacher,Course,Course_Teach_Stu,_class
from app import db

@student.route('/index')
@login_required
@permission_required(Permission.STUDENT_INFO)
def index():

    return render_template('student/index.html',mainUrl='mainData')

@student.route('/mainData')
@login_required
@permission_required(Permission.STUDENT_INFO)
def mainData():
    data = {'dataUrl':'data','operateUrls':'','dataFieldes':[],'dataTitles':[],'addFieldes':[],'editFieldes':[]}
    if current_user.type == 0:
        return getDataForStudent()
    if current_user.type == 1:
        data['dataTitles'] = ['姓名','学号','性别','班级','课程名','学期']
        data['dataFieldes'] = ['StudentName','StudentId','Sex','ClassName','CourseName','Semester']
    if current_user.type == 2:
        data['operateUrls'] = {'addUrl':'addStudent','editUrl':'editStudent','delUrl':'delStudent'}
        data['dataTitles'] = ['Id','姓名','学号','性别','班级','班级ID','密码']
        data['dataFieldes'] = ['Id','StudentName','StudentId','Sex','ClassName','ClassId','Passwd']
        data['addFieldes'] = ['StudentName','StudentId','Sex','ClassId','Passwd']
        data['editFieldes'] = ['StudentName','StudentId','Sex','ClassId','Passwd']

    return json.dumps(data)

@student.route('/data')
@login_required
@permission_required(Permission.STUDENT_INFO)
def data():

    if current_user.type == 1:
        return getDataForTeacher()
    if current_user.type == 2:
        return getDataForAdmin()

    return None

@permission_required(RolePermission.TEACHER)
def getDataForTeacher():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','StudentName')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getCoursesInfo()

    targetDict = {'StudentName':Student.name,'StudentId':Student.id,'Sex':Student.sex,'ClassName':_class.name,'CourseName':Course.name,'Semester':Course.semester}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'StudentName')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'StudentName')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)
    datas = []
    oldItem = []
    for item in pagination.items :
        temp = {'StudentName':item[0].name,'StudentId':item[0].id,'Sex':item[0].sex,'ClassName':item[4].name,'CourseName':item[2].name,'Semester':item[2].semester}
        datas.append(temp)

    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@permission_required(RolePermission.ADMIN)
def getDataForAdmin():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','name')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getAllStudent()

    targetDict = {'StudentName':Student.name,'StudentId':Student.id,'Sex':Student.sex,'Id':Student._id,'ClassId':_class._id,'ClassName':_class.name}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'name')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'name')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)

    datas = []
    for item in pagination.items :

        temp = {'StudentName':item[0].name,'StudentId':item[0].id,'Sex':item[0].sex,'Id':item[0]._id,'ClassId':item[1]._id,'ClassName':item[1].name,'Passwd':''}
        datas.append(temp)

    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@student.route('/editStudent',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def editStudent():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        student = db.session.query(Student).filter(Student._id==id).first()

        student.id = request.form.get('StudentId',student.id)
        student.name = request.form.get('StudentName',student.name)
        student.sex = str_to_bool(request.form.get('Sex',student.sex))
        student._class = request.form.get('ClassId',student._class)


        if(request.form.get('Passwd','')!=''):
            student.passwd = request.form.get('Passwd')


        db.session.add(student)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '修改失败'
        print(e)
    return str(json.dumps(result))

@student.route('/addStudent',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def addStudent():
    result={'code':1,'result':'success'}
    try:
        student = Student()

        student.id = request.form.get('StudentId',student.id)
        student.name = request.form.get('StudentName',student.name)
        student.sex = str_to_bool(request.form.get('Sex',student.sex))


        if(request.form.get('ClassId','')!=''):
            student._class = int(request.form.get('ClassId'))
        if(request.form.get('Passwd','')!=''):
            student.passwd = request.form.get('Passwd')
            
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '添加失败'
        print(e)
    return str(json.dumps(result))

@student.route('/delStudent',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def delStudent():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        student = db.session.query(Student).filter(Student._id==id).first()
        db.session.delete(student)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '删除失败'
        print(e)
    return str(json.dumps(result))

def str_to_bool(str):
    if str.lower() == 'true':
        return True
    if str.lower() == 'false':
        return False
    return None

