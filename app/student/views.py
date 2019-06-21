from . import student
from .forms import StuForm
from flask import render_template,flash,redirect,url_for
from flask_login import login_user,current_user,login_required,logout_user
from app.decorators import permission_required
from config import Permission

@student.route('/index')
@login_required
@permission_required(Permission.STUDENT_INFO)
def index():
    stuForm = StuForm()
    return render_template('student/index.html',form=stuForm)