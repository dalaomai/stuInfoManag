from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,PasswordField,SubmitField,SelectField,BooleanField
from wtforms.validators import Required,Length

class StuForm(FlaskForm):
    id = StringField("ID",validators=[Required()])
    passwd = PasswordField("Password",validators=[Required()])
    type = SelectField("角色",choices=[(0,"学生"),(1,'老师'),(2,'管理员')],coerce=int)
    remember = BooleanField("记住登陆")
    submit = SubmitField("Login in")