from . import teacher

from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,current_user,login_required,logout_user
from config import Config
from app.decorators import permission_required
from config import Permission,RolePermission
import json
from sqlalchemy import desc,asc
from app.models import Student,Teacher,Course,Course_Teach_Stu
from app import db

@teacher.route('/index')
@login_required
@permission_required(Permission.TEACHER_INFO)
def index():

    return render_template('teacher/index.html',mainUrl='mainData')

@teacher.route('/mainData')
@login_required
@permission_required(Permission.TEACHER_INFO)
def mainData():
    data = {'dataUrl':'data','operateUrls':'','dataFieldes':[],'dataTitles':[],'addFieldes':[],'editFieldes':[]}

    if current_user.type == 2:
        data['operateUrls'] = {'addUrl':'addTeacher','editUrl':'editTeacher','delUrl':'delTeacher'}
        data['dataTitles'] = ['Id','姓名','工号','性别','密码']
        data['dataFieldes'] = ['Id','TeacherName','TeacherId','Sex','Passwd']
        data['addFieldes'] = ['TeacherName','TeacherId','Sex','Passwd']
        data['editFieldes'] = ['TeacherName','TeacherId','Sex','Passwd']

    return json.dumps(data)

@teacher.route('/data')
@login_required
@permission_required(Permission.TEACHER_INFO)
def data():

    if current_user.type == 2:
        return getDataForAdmin()

    return None


@permission_required(RolePermission.ADMIN)
def getDataForAdmin():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','TeacherName')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getAllTeacher()

    targetDict = {'TeacherName':Teacher.name,'TeacherId':Teacher.id,'Sex':Teacher.sex,'Id':Teacher._id}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'TeacherName')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'TeacherName')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)

    datas = []
    for item in pagination.items :

        temp = {'TeacherName':item.name,'TeacherId':item.id,'Sex':item.sex,'Id':item._id,'Passwd':''}
        datas.append(temp)

    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@teacher.route('/editTeacher',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def editTeacher():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        teacher = db.session.query(Teacher).filter(Teacher._id==id).first()

        teacher.id = request.form.get('TeacherId',teacher.id)
        teacher.name = request.form.get('TeacherName',teacher.name)
        teacher.sex = str_to_bool(request.form.get('Sex',teacher.sex))

        if(request.form.get('Passwd','')!=''):
            teacher.passwd = request.form.get('Passwd')


        db.session.add(teacher)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '修改失败'
        print(e)
    return str(json.dumps(result))

@teacher.route('/addTeacher',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def addTeacher():
    result={'code':1,'result':'success'}
    try:
        teacher = Teacher()
        teacher.id = request.form.get('TeacherId',teacher.id)
        teacher.name = request.form.get('TeacherName',teacher.name)
        teacher.sex = str_to_bool(request.form.get('Sex',teacher.sex))

        if(request.form.get('Passwd','')!=''):
            teacher.passwd = request.form.get('Passwd')
            
        db.session.add(teacher)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '添加失败'
        print(e)
    return str(json.dumps(result))

@teacher.route('/delTeacher',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def delTeacher():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        teacher = db.session.query(Teacher).filter(Teacher._id==id).first()
        db.session.delete(teacher)
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

