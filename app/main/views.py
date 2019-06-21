from flask import render_template, session, redirect, url_for, current_app
from flask_login import current_user,login_required
from app import db



from app.main import main


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    
    return render_template('index.html')
