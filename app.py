from flask import Flask,session,g,render_template, redirect
import config
from exts import db, mail
from models import UserModel
from blueplants.qa import bp as qa_bp
from blueplants.auth import bp as auth_bp
from flask_migrate import Migrate
from flask_socketio import SocketIO


app = Flask(__name__)


app.config.from_object(config)
app.secret_key= config.secret_key


db.init_app(app)
mail.init_app(app)

migrade = Migrate(app, db)
'''
建表：
flask db init(执行一次即可)
flask db migrate(检查变化)
flask db upgrade(更改数据库)
'''

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

socketio = SocketIO(app)


@app.before_request
def my_befor_request():
    if "user_id" in session:
        user_id = session["user_id"]
        user = UserModel.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user":g.user}



@app.route('/')
def hello_world():  # put application's code here
    return render_template('html/home.html')
    # return redirect('/qa')



if __name__ == '__main__':
    socketio.run()
