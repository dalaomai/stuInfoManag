from flask import render_template, session, redirect, url_for, current_app
from app import db



from app.main import main


@main.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')
