from . import aclass

from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,current_user,login_required,logout_user
from config import Config
from app.decorators import permission_required
from config import Permission,RolePermission
import json
from sqlalchemy import desc,asc
from app.models import Student,Teacher,Course,Course_Teach_Stu,_class
from app import db

@aclass.route('/index')
@login_required
@permission_required(Permission.CLASS_INFO)
def index():

    return render_template('class/index.html',mainUrl='mainData')

@aclass.route('/mainData')
@login_required
@permission_required(Permission.CLASS_INFO)
def mainData():
    data = {'dataUrl':'data','operateUrls':'','dataFieldes':[],'dataTitles':[],'addFieldes':[],'editFieldes':[]}

    if current_user.type == 2:
        data['operateUrls'] = {'addUrl':'addClass','editUrl':'editClass','delUrl':'delClass'}
        data['dataTitles'] = ['Id','班级']
        data['dataFieldes'] = ['Id','ClassName']
        data['addFieldes'] = ['ClassName']
        data['editFieldes'] = ['ClassName']

    return json.dumps(data)

@aclass.route('/data')
@login_required
@permission_required(Permission.CLASS_INFO)
def data():

    if current_user.type == 2:
        return getDataForAdmin()

    return None


@permission_required(RolePermission.ADMIN)
def getDataForAdmin():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','ClassName')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getAllClass()

    targetDict = {'ClassName':_class.name,'Id':_class._id}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'ClassName')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'ClassName')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)

    datas = []
    for item in pagination.items :

        temp = {'ClassName':item.name,'Id':item._id}
        datas.append(temp)

    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@aclass.route('/editClass',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def editClass():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        aclass = db.session.query(_class).filter(_class._id==id).first()

        aclass.name = request.form.get('ClassName',aclass.name)



        db.session.add(aclass)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '修改失败'
        print(e)
    return str(json.dumps(result))

@aclass.route('/addClass',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def addClass():
    result={'code':1,'result':'success'}
    try:
        aclass = _class()
        aclass.name = request.form.get('ClassName',aclass.name)

        if(request.form.get('Passwd','')!=''):
            teacher.passwd = request.form.get('Passwd')
            
        db.session.add(aclass)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '添加失败'
        print(e)
    return str(json.dumps(result))

@aclass.route('/delClass',methods=['POST'])
@login_required 
@permission_required(RolePermission.ADMIN)
def delClass():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        alcass = db.session.query(_class).filter(_class._id==id).first()
        db.session.delete(alcass)
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

