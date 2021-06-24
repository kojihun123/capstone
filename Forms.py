from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo, Email
from Models import User 
from werkzeug.security import check_password_hash

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email('이메일 형식으로 작성해주세요')])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('password_2', '같은 비밀번호를 입력해주세요')]) 
    password_2 = PasswordField('password_2', validators=[DataRequired()])

class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
            
        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data
            usertable = User.query.filter_by(userid=userid).first()
            if not usertable:
                raise ValueError('아이디가 존재하지 않거나 비밀번호가 틀렸습니다.')
            elif not check_password_hash(usertable.password, password):
                raise ValueError('아이디가 존재하지 않거나 비밀번호가 틀렸습니다.')
                
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])

class Postform(FlaskForm):
    userid = StringField('userid')
    writer = StringField('writer')
    market = StringField('market')
    address = StringField('address')
    type = StringField('type')
    point = StringField('point')
    contents = StringField('contents')