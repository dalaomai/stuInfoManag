from app.course import course

from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,current_user,login_required,logout_user
from config import Config
from app.decorators import permission_required
from config import Permission,RolePermission
import json
from sqlalchemy import desc,asc
from app.models import Student,Teacher,Course,Course_Teach_Stu
from app import db

@course.route('/index')
@login_required
@permission_required(Permission.COURSE_INFO)
def index():
    tableFile = 'student.js'
    if current_user.type == 0:
        tableFile = 'student.js'
    if current_user.type == 1:
        tableFile = 'teacher.js'
    if current_user.type == 2:
        tableFile = 'admin.js'

    return render_template('course/index.html',tableFile=tableFile)

@course.route('/data')
@login_required
@permission_required(Permission.COURSE_INFO)
def data():
    if current_user.type == 0:
        return getDataForStudent()
    if current_user.type == 1:
        return getDataForTeacher()
    if current_user.type == 2:
        return getDataForAdmin()

    return None

@course.route('/delCourse',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def delCourse():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        course = db.session.query(Course).filter(Course._id==id).first()
        db.session.delete(course)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '删除失败'
        print(e)
    return str(json.dumps(result))

@course.route('/editCourse',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def editCourse():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        course = db.session.query(Course).filter(Course._id==id).first()
        course.id = request.form.get('CourseId',course.id)
        course.name = request.form.get('CourseName',course.name)
        course.college = request.form.get('College',course.college)


        db.session.add(course)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '修改失败'
        print(e)
    return str(json.dumps(result))

@course.route('/addCourse',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def addCourse():
    result={'code':1,'result':'success'}
    try:
        course = Course()
        course.id = request.form.get('CourseId')
        course.name = request.form.get('CourseName')
        course.college = request.form.get('College')
            
        db.session.add(course)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '添加失败'
        print(e)
    return str(json.dumps(result))

@permission_required(RolePermission.STUDENT)
def getDataForStudent():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','CourseName')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getCoursesInfo()

    targetDict = {'CourseName':Course.name,'TeacherName':Teacher.name,'Source':Course_Teach_Stu.source,'College':Course.college,'CourseId':Course.id}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'CourseName')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'CourseName')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)
    datas = []
    for item in pagination.items :
        temp = {'CourseName':item[2].name,'TeacherName':item[1].name,'Source':item[3].source,'College':item[2].college,'CourseId':item[2].id}
        datas.append(temp)
    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@permission_required(RolePermission.TEACHER)
def getDataForTeacher():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','CourseName')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getCoursesInfo()

    targetDict = {'CourseName':Course.name,'StudentName':Student.name,'Class':Student._class,'College':Course.college,'CourseId':Course.id}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'CourseName')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'CourseName')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)
    datas = []
    oldItem = []
    for item in pagination.items :
        if oldItem==[]:
            temp = {'CourseName':item[2].name,'Class':item[0]._class,'College':item[2].college,'CourseId':item[2].id}
            datas.append(temp)
            oldItem = item
            continue

        if oldItem[0]._class != item[0]._class and  item[2] != oldItem[2]:
            temp = {'CourseName':item[2].name,'Class':item[0]._class,'College':item[2].college,'CourseId':item[2].id}
            datas.append(temp)
        oldItem = item

    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@permission_required(RolePermission.ADMIN)
def getDataForAdmin():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','CourseName')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getAllCourse()

    targetDict = {'CourseName':Course.name,'CourseId':Course.id,'College':Course.college,'Id':Course._id}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'CourseName')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'CourseName')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)
    datas = []
    oldItem = []
    for item in pagination.items :
        if oldItem != item:
            temp = {'CourseName':item.name,'CourseId':item.id,'College':item.college,'Id':item._id}
            datas.append(temp)
        oldItem = item
    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))