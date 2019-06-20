from flask import render_template,flash,redirect,url_for
from flask_login import login_user,current_user,login_required,logout_user
from . import auth
from app.auth.forms import LoginForm
from app.models import User

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    #进入登陆页面
    if not form.validate_on_submit():
        return render_template('auth/login.html',form = form)
    #登陆
    user = User.query_user([form.type.data,form.id.data])
    if user is not None and user.verify_passwd(form.passwd.data):
        login_user(user,form.remember.data)
        flash("登陆成功" + str(current_user.type))
    else:
        flash("登陆失败",'error')
    return render_template('auth/login.html',form = form)

@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("已退出登陆!")
    return redirect(url_for("main.index"))
