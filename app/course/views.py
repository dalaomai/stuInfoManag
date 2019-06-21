from app.course import course
from app.course.forms import StuForm
from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,current_user,login_required,logout_user
from config import Config

@course.route('/index')
@login_required
def index():
    page = request.args.get('page',1,type=int)
    pagination = current_user.getCoursesInfo().paginate(page,per_page=Config.POSTS_PER_PAGE,error_out=False)
    return render_template('course/index.html',pagination=pagination)