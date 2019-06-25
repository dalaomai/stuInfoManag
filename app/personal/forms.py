from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,PasswordField,SubmitField,SelectField,BooleanField,widgets
from wtforms.validators import Required,Length,EqualTo

class StuForm(FlaskForm):
    stype = StringField("角色",render_kw={'readonly':'readonly'})
    id = StringField("学号",render_kw={'readonly':'readonly'})
    aclass = StringField("班级",render_kw={'readonly':'readonly'})
    sex = StringField("性别",render_kw={'readonly':'readonly'})

    passwd = PasswordField("Password")
    passwd2 = PasswordField("Confirm Password",validators=[EqualTo('passwd',message='密码不一致')])

    submit = SubmitField("修改信息")
    
    def __init__(self,stu):
        super().__init__()
        self.stype.data = "学生"
        self.id.data= stu.id
        self.aclass.data = stu.aclass.name
        if stu.sex == 0:
            self.sex.data = '男'
        if stu.sex:
            self.sex.data = '女'
        
class TeachForm(FlaskForm):
    stype = StringField("角色",render_kw={'readonly':'readonly'})
    id = StringField("工号",render_kw={'readonly':'readonly'},)
    sex = StringField("性别",render_kw={'readonly':'readonly'})

    passwd = PasswordField("Password")
    passwd2 = PasswordField("Confirm Password",validators=[EqualTo('passwd',message='密码不一致')])

    submit = SubmitField("修改信息")
    
    def __init__(self,user):
        super().__init__()
        self.stype.data = "老师"
        self.id.data= user.id
        if user.sex == 0:
            self.sex.data = '男'
        if user.sex:
            self.sex.data = '女'

class AdminForm(FlaskForm):
    stype = StringField("角色",render_kw={'readonly':'readonly'})
    id = StringField("工号",render_kw={'readonly':'readonly'},)
    sex = StringField("性别",render_kw={'readonly':'readonly'})

    passwd = PasswordField("Password")
    passwd2 = PasswordField("Confirm Password",validators=[EqualTo('passwd',message='密码不一致')])

    submit = SubmitField("修改信息")
    
    def __init__(self,user):
        super().__init__()
        self.stype.data = "管理员"
        self.id.data= user.id
        if user.sex == 0:
            self.sex.data = '男'
        if user.sex:
            self.sex.data = '女'