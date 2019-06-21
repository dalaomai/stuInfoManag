from . import personal
from .forms import StuForm,TeachForm,AdminForm
from flask import render_template,flash,redirect,url_for
from flask_login import login_user,current_user,login_required,logout_user
from app.decorators import permission_required
from config import Permission
from app.models import Student,Teacher,Admin

@personal.route('/index',methods=['GET','POST'])
@login_required
@permission_required(Permission.PERSONAL_INFO)
def index():
    if current_user.type == 0:
        form = StuForm(current_user)
    elif current_user.type == 1:
        form = TeachForm(current_user)
    elif current_user.type == 2:
        form = AdminForm(current_user)

    if form.validate_on_submit():
        result = current_user.modifyBaseInfo(form.passwd.data)
        if result == None:
            flash("修改成功")
        else:
            flash("修改失败")

    return render_template('personal/index.html',form=form)

