import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel, EmailCaptchaModel
from werkzeug.security import generate_password_hash,check_password_hash


# 验证表单
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(min=4,max=4,message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    # 自定义验证
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_base = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha == captcha_base:
            raise wtforms.ValidationError(message="邮箱或验证码错误")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message="标题长度应在3到100之间")])
    content = wtforms.StringField(validators=[Length(min=3,message="内容用大于3")])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1,message="内容需要大于0")])
