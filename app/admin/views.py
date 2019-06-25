from . import admin

from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,current_user,login_required,logout_user
from config import Config
from app.decorators import permission_required
from config import Permission,RolePermission
import json
from sqlalchemy import desc,asc
from app.models import Student,Teacher,Course,Course_Teach_Stu,Admin
from app import db

@admin.route('/index')
@login_required
@permission_required(Permission.ADMIN_INFO)
def index():

    return render_template('admin/index.html',mainUrl='mainData')

@admin.route('/mainData')
@login_required
@permission_required(Permission.ADMIN_INFO)
def mainData():
    data = {'dataUrl':'data','operateUrls':'','dataFieldes':[],'dataTitles':[],'addFieldes':[],'editFieldes':[]}
    if current_user.type == 0:
        return getDataForStudent()
    if current_user.type == 1:
        return getDataForTeacher()
    if current_user.type == 2:
        data['operateUrls'] = {'addUrl':'addAdmin','editUrl':'editAdmin','delUrl':'delAdmin'}
        data['dataTitles'] = ['Id','姓名','工号','性别','权限','密码']
        data['dataFieldes'] = ['Id','AdminName','AdminId','Sex','Permission','Passwd']
        data['addFieldes'] = ['AdminName','AdminId','Sex','Passwd']
        data['editFieldes'] = ['AdminName','AdminId','Sex','Passwd']

    return json.dumps(data)

@admin.route('/data')
@login_required
@permission_required(Permission.ADMIN_INFO)
def data():

    if current_user.type == 2:
        return getDataForAdmin()

    return None


@permission_required(RolePermission.ROOT)
def getDataForAdmin():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','AdminName')
    sortOrder = request.args.get('sortOrder','asc')
    queryResult = current_user.getAllAdmin()

    targetDict = {'AdminName':Admin.name,'AdminId':Admin.id,'Sex':Admin.sex,'Id':Admin._id,'Permission':Admin.permission}
    if sortOrder=='asc':
        queryResult = queryResult.order_by(asc(targetDict.get(sort,'AdminName')))
    else:
        queryResult = queryResult.order_by(desc(targetDict.get(sort,'AdminName')))
    

    pagination = queryResult.paginate(page,per_page=rows,error_out=False)

    datas = []
    for item in pagination.items :

        temp = {'AdminName':item.name,'AdminId':item.id,'Sex':item.sex,'Id':item._id,'Passwd':'','Permission':item.permission}
        datas.append(temp)

    datas = {'total':pagination.total,'rows':datas}
    return str(json.dumps(datas))

@admin.route('/editAdmin',methods=['POST'])
@login_required 
@permission_required(RolePermission.ROOT)
def editAdmin():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        admin = db.session.query(Admin).filter(Admin._id==id).first()

        admin.id = request.form.get('AdminName',admin.id)
        admin.name = request.form.get('Name',admin.name)
        admin.sex = str_to_bool(request.form.get('Sex',admin.sex))


        if(request.form.get('Passwd','')!=''):
            admin.passwd = request.form.get('Passwd')
        if(request.form.get('Permission','')!=''):
            admin.permission = request.form.get('Permission')


        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '修改失败'
        print(e)
    return str(json.dumps(result))

@admin.route('/addAdmin',methods=['POST'])
@login_required 
@permission_required(RolePermission.ROOT)
def addAdmin():
    result={'code':1,'result':'success'}
    try:
        admin = Admin()
        admin.id = request.form.get('AdminId',admin.id)
        admin.name = request.form.get('AdminName',admin.name)
        admin.sex = str_to_bool(request.form.get('Sex',admin.sex))

        if(request.form.get('Passwd','')!=''):
            admin.passwd = request.form.get('Passwd')
        if(request.form.get('Permission','')!=''):
            admin.passwd = request.form.get('Permission')
            
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        result['code'] = 0
        result['result'] = '添加失败'
        print(e)
    return str(json.dumps(result))

@admin.route('/delAdmin',methods=['POST'])
@login_required 
@permission_required(RolePermission.ROOT)
def delAdmin():
    result={'code':1,'result':'success'}
    try:
        id = request.form.get('Id',None)
        if(id==current_user._id):
            result['code'] = 0
            result['result'] = '不能把自己删了'
            return result

        admin = db.session.query(Admin).filter(Admin._id==id).first()
        db.session.delete(admin)
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

