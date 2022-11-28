from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def index():
    """Return homepage."""

    return render_template("start.html", survey=survey)


@app.route('/begin', methods=['POST'])
def start_survey():
    """Clears session and redirect to question"""

    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Shows the question"""

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)
