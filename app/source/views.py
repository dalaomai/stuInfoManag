from . import source

from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,current_user,login_required,logout_user
from config import Config
from app.decorators import permission_required
from config import Permission,RolePermission
import json
from sqlalchemy import desc,asc,and_
from app.models import Student,Teacher,Course,Course_Teach_Stu,_class
from app import db

@source.route('/index')
@login_required
@permission_required(Permission.SOURCE_INFO)
def index():

    return render_template('source/index.html',mainUrl='mainData')

@source.route('/mainData')
@login_required
@permission_required(Permission.SOURCE_INFO)
def mainData():
    data = {'dataUrl':'data','operateUrls':'','dataFieldes':[],'dataTitles':[],'addFieldes':[],'editFieldes':[]}

    if current_user.type == 1:
        data['operateUrls'] = {'addUrl':'','editUrl':'editSource','delUrl':''}
        data['dataTitles'] = ['Id','姓名','学号','性别','班级','班级ID','课程名','课程ID','开课学期','成绩']
        data['dataFieldes'] = ['Id','StudentName','StudentId','Sex','ClassName','ClassId','CourseName','CourseId','Semester','Source']
        data['editFieldes'] = ['Source']
    if current_user.type == 2:
        data['operateUrls'] = {'addUrl':'addSource','editUrl':'editSource','delUrl':'delSource'}
        data['dataTitles'] = ['Id','姓名','学号','性别','班级','班级ID','老师','老师工号','课程名','课程ID','开课学期','成绩']
        data['dataFieldes'] = ['Id','StudentName','StudentId','Sex','ClassName','ClassId','TeacherName','TeacherId','CourseName','CourseId','Semester','Source']
        data['addFieldes'] = ['StudentId','TeacherId','CourseId','Source']
        data['editFieldes'] = ['StudentId','TeacherId','CourseId','Source']

    return json.dumps(data)

@source.route('/data')
@login_required
@permission_required(Permission.SOURCE_INFO)
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

    targetDict = {'StudentName':Student.name,'StudentId':Student.id,'ClassId':_class._id,'CourseName':Course.name,'CourseId':Course.id,'Source':Course_Teach_Stu.source,'Semester':Course.semester,'ClassName':_class.name,'Id':Course_Teach_Stu._id}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'StudentName')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'StudentName')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)

    datas = []
    for item in pagination.items :

        temp = {'StudentName':item[0].name,'StudentId':item[0].id,'ClassId':item[4]._id,'CourseName':item[2].name,'CourseId':item[2].id,'Source':item[3].source,'Semester':item[2].semester,'ClassName':item[4].name,'Id':item[3]._id}
        datas.append(temp)

    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@permission_required(RolePermission.ADMIN)
def getDataForAdmin():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','Id')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getCoursesInfo()

    targetDict = {'StudentName':Student.name,'StudentId':Student.id,'ClassId':_class._id,'CourseName':Course.name,'CourseId':Course.id,'Source':Course_Teach_Stu.source,'Id':Course_Teach_Stu._id,'TeacherId':Teacher.id,'TeacherName':Teacher.name,'Semester':Course.semester,'ClassName':_class.name}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'name')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'name')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)

    datas = []
    for item in pagination.items :

        temp = {'StudentName':item[0].name,'StudentId':item[0].id,'ClassId':item[4]._id,'CourseName':item[2].name,'CourseId':item[2].id,'Source':item[3].source,'Id':item[3]._id,'TeacherId':item[1].id,'TeacherName':item[1].name,'Semester':item[2].semester,'ClassName':item[4].name}
        datas.append(temp)

    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@source.route('/editSource',methods=['POST'])
@login_required 
@permission_required(RolePermission.TEACHER)
def editSource():
    if(current_user.type==1):
        return editSourceForTeacher()
    if(current_user.type==2):
        return editSourceForAdmin()

@permission_required(RolePermission.TEACHER)
def editSourceForTeacher():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)

        course_teach_stu = db.session.query(Course_Teach_Stu).filter(and_(Course_Teach_Stu._id==id,Course_Teach_Stu.teach==current_user.id)).first()

        course_teach_stu.source = request.form.get('Source',course_teach_stu.source)
        
        db.session.add(course_teach_stu)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '修改失败'
        print(e)
    return str(json.dumps(result))   

@permission_required(RolePermission.ADMIN)
def editSourceForAdmin():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        course_teach_stu = db.session.query(Course_Teach_Stu).filter(Course_Teach_Stu._id==id).first()
        course_teach_stu.source = request.form.get('Source',course_teach_stu.source)
        course_teach_stu.stu = request.form.get('StudentId',course_teach_stu.stu)
        course_teach_stu.teach = request.form.get('TeacherId',course_teach_stu.teach)
        course_teach_stu.course = request.form.get('CourseId',course_teach_stu.course)
        
        db.session.add(course_teach_stu)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '修改失败'
        print(e)
    return str(json.dumps(result))   

@source.route('/addSource',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def addSource():
    result={'code':1,'result':'success'}
    try:
        course_teach_stu = Course_Teach_Stu()

        course_teach_stu.stu = request.form.get('StudentId',course_teach_stu.stu)
        course_teach_stu.teach = request.form.get('TeacherId',course_teach_stu.teach)
        course_teach_stu.course = request.form.get('CourseId',course_teach_stu.course)
        course_teach_stu.source = request.form.get('Source',course_teach_stu.source)
        if(course_teach_stu.source==''):
            course_teach_stu.source=None


            
        db.session.add(course_teach_stu)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '添加失败'
        print(e)
    return str(json.dumps(result))

@source.route('/delSource',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def delSource():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        course_teach_stu = db.session.query(Course_Teach_Stu).filter(Course_Teach_Stu._id==id).first()
        db.session.delete(course_teach_stu)
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

