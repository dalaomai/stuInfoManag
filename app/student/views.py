from . import student

from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,current_user,login_required,logout_user
from config import Config
from app.decorators import permission_required
from config import Permission,RolePermission
import json
from sqlalchemy import desc,asc
from app.models import Student,Teacher,Course,Course_Teach_Stu
from app import db

@student.route('/index')
@login_required
@permission_required(Permission.STUDENT_INFO)
def index():
    if current_user.type == 1:
        tableFile = 'teacher.js'
    if current_user.type == 2:
        tableFile = 'admin.js'

    return render_template('student/index.html',tableFile=tableFile)

@student.route('/data')
@login_required
@permission_required(Permission.STUDENT_INFO)
def data():

    if current_user.type == 1:
        return getDataForTeacher()
    if current_user.type == 2:
        return getDataForAdmin()

    return None

@permission_required(RolePermission.ADMIN)
def getDataForAdmin():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','name')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getAllStudent()

    targetDict = {'Name':Student.name,'StudentId':Student.id,'Sex':Student.sex,'Id':Student._id,'_class':Student._class,'Permission':Student.permission}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'name')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'name')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)

    datas = []
    for item in pagination.items :

        temp = {'Name':item.name,'StudentId':item.id,'Sex':item.sex,'Id':item._id,'_class':item._class,'Permission':item.permission,'Passwd':''}
        datas.append(temp)

    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@student.route('/editCourse',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def editCourse():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        student = db.session.query(Student).filter(Student._id==id).first()

        student.id = request.form.get('StudentId',student.id)
        student.name = request.form.get('Name',student.name)
        student.sex = str_to_bool(request.form.get('Sex',student.sex))
        student._class = request.form.get('_class',student._class)
        student.permission = request.form.get('Permission',student.permission)
        if(request.form.get('Passwd','')!=''):
            student.passwd = request.form.get('Passwd')


        db.session.add(student)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '修改失败'
        print(e)
    return str(json.dumps(result))

@student.route('/addCourse',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def addCourse():
    result={'code':1,'result':'success'}
    try:
        student = Student()
        student.id = request.form.get('StudentId',student.id)
        student.name = request.form.get('Name',student.name)
        student.sex = str_to_bool(request.form.get('Sex',student.sex))
        student._class = request.form.get('_class',student._class)
        student.permission = request.form.get('Permission',student.permission)
        if(request.form.get('Passwd','')!=''):
            student.passwd = request.form.get('Passwd')
            
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '添加失败'
        print(e)
    return str(json.dumps(result))

def str_to_bool(str):
    if str.lower() == 'true':
        return True
    if str.lower() == 'false':
        return False
    return None

