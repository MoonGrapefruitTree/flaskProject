from flask import Blueprint, request, render_template, g, redirect
from .forms import QuestionForm, AnswerForm
from models import QuestionMOdel, AnswerModel
from exts import db
from decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/qa")


@bp.route('/', methods=["GET", "POST"])
def qaIndex():
    questions = QuestionMOdel.query.order_by(QuestionMOdel.create_time.desc()).all()
    return render_template("html/qahome.html", questions=questions)


@bp.route('/detail', methods=["get", "POST"])
def get_detail():
    question_id = request.args.get("question_id")
    question = QuestionMOdel.query.filter_by(id=question_id).first()
    return render_template("html/detail.html", question=question)


@bp.route('/publicAns', methods=["POST"])
@login_required
def publicAns():
    question_id = request.args.get("question_id")
    question = QuestionMOdel.query.filter_by(id=question_id).first()
    if request.method == "POST":
        form = AnswerForm(request.form)
        if form.validate():
            content = form.content.data
            new_ans = AnswerModel(content=content, question=question, author=g.user)
            db.session.add(new_ans)
            db.session.commit()
    return redirect("/qa/detail?question_id=" + question_id)


@bp.route('/publicNew', methods=["GET", "POST"])
@login_required
def public_qa():
    if request.method == "GET":
        return render_template('html/publicNewQA.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            new_question = QuestionMOdel(title=title, content=content, author=g.user)
            db.session.add(new_question)
            db.session.commit()
            return redirect("/qa")
        else:
            return redirect("/qa/publicNew")


@bp.route('/search', methods=["POST"])
def search():

    q = request.form.get("search_input")
    if q:
        questions = QuestionMOdel.query.filter(QuestionMOdel.title.contains(q)).all()
        return render_template("html/qahome.html", questions=questions)
    else:
        return redirect('/qa')

