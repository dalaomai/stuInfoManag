from . import statistic

from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,current_user,login_required,logout_user
from config import Config
from app.decorators import permission_required
from config import Permission,RolePermission
import json
from sqlalchemy import desc,asc
from app.models import Student,Teacher,Course,Course_Teach_Stu,Admin
from app import db

@statistic.route('/student')
@login_required
@permission_required(Permission.STATISTIC_INFO)
def studentStatistic():
    return render_template('statistic/index.html',mainUrl='mainStudentData')

@statistic.route('/mainStudentData')
@login_required
@permission_required(Permission.STATISTIC_INFO)
def mainStudentData():
    data = {'dataUrl':'studentDataForAdmin','operateUrls':'','dataFieldes':[],'dataTitles':[],'addFieldes':[],'editFieldes':[]}
    if current_user.type == 2:
        data['dataTitles'] = ['学号','姓名','班级','学期','平均分']
        data['dataFieldes'] = ['StudentId','StudentName','ClassName','Semester','GAvg']
    return json.dumps(data)

@statistic.route('/studentDataForAdmin')
@login_required
@permission_required(RolePermission.ADMIN)
def studentDataForAdmin():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','StudentId')
    sortOrder = request.args.get('sortOrder','asc')
     
    selectResult = db.session.execute('select * from stu_semes order by ' + sort + ' ' + sortOrder + ' limit ' + str(rows*(page-1)) + ',' + str(rows))

    datas = []
    oldItem = []
    for item in selectResult :

        temp = {'StudentId':item[0],'StudentName':item[1],'ClassName':item[2],'Semester':item[3],'GAvg':str(item[4])}
        datas.append(temp)

    datas = {'total':next(db.session.execute('select count(*) from stu_semes'))[0],'rows':datas}
    return str(json.dumps(datas))    


@statistic.route('/class')
@login_required
@permission_required(Permission.STATISTIC_INFO)
def classStatistic():
    return render_template('statistic/index.html',mainUrl='mainClassData')

@statistic.route('/mainClassData')
@login_required
@permission_required(Permission.STATISTIC_INFO)
def mainClassData():
    data = {'dataUrl':'classDataForAdmin','operateUrls':'','dataFieldes':[],'dataTitles':[],'addFieldes':[],'editFieldes':[]}
    if current_user.type == 2:
        data['dataTitles'] = ['班级ID','班级','学期','课程名','平均分','最高分','最低分','及格人数','及格率(%)']
        data['dataFieldes'] = ['ClassId','ClassName','Semester','CourseName','GAvg','GMax','GMin','PassNumber','PassRate']
    return json.dumps(data)

@statistic.route('/classDataForAdmin')
@login_required
@permission_required(RolePermission.ADMIN)
def classDataForAdmin():
    page = request.args.get('page',1,type=int)
    rows = request.args.get('rows',Config.POSTS_PER_PAGE,type=int)
    sort = request.args.get('sort','ClassId')
    sortOrder = request.args.get('sortOrder','asc')
     
    selectResult = db.session.execute('select * from class_semes order by ' + sort + ' ' + sortOrder + ' limit ' + str(rows*(page-1)) + ',' + str(rows))

    datas = []
    oldItem = []
    for item in selectResult :

        temp = {'ClassId':item[0],'ClassName':item[1],'Semester':item[2],'CourseName':item[3],'GAvg':str(item[4]),'GMax':str(item[5]),'GMin':str(item[6]),'PassNumber':str(item[7]),'PassRate':str(item[8])}
        datas.append(temp)

    datas = {'total':next(db.session.execute('select count(*) from class_semes'))[0],'rows':datas}
    return str(json.dumps(datas))    