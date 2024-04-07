import random
from models import EmailCaptchaModel, UserModel
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
import string
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash,check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("html/login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            print(email)
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("用户不存在")
                return redirect("/auth/login")
            else:
                if check_password_hash(user.password,password):
                    session['user_id'] = user.id
                    return redirect('/qa')
                else:
                    print("密码错误")
                    return redirect("/auth/login")
        else:
            print(form.errors)
            return "输入信息格式错误，登录失败"


@bp.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("html/register.html")
    else:
        # 后端验证表单
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # return redirect("/auth/login")
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect("/auth/register")


@bp.route("/logout")
def get_logout():
    session.clear()
    return redirect('/')


@bp.route("/captcha/email")
def get_email_captcha():
    # 获得参数
    # 前端/captcha/email?email=xxx@xxx.com
    email = request.args.get("email")
    # 生成验证码
    source = string.digits*4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    # 发送信息
    message = Message(subject="邮箱验证", recipients=[email], body="您正在注册HS的项目，验证码是："+captcha+"。请勿向他人泄露。")
    mail.send(message)
    # 临时储存
    email_exist = EmailCaptchaModel.query.filter_by(email=email).first()
    if email_exist:
        email_exist.captcha = captcha
        db.session.add(email_exist)
        db.session.commit()
    else:
        email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()
    # return "success"
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="hello", recipients=["18811718913@163.com"], body="这是测试邮件")
    mail.send(message)
    return "成功"