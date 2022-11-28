from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

CURRENT_SURVEY_KEY = "current_survey"
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


@app.route("/answer", methods=["POST"])
def handle_question():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Shows the question"""
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        return redirect("/")
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)


@app.route("/complete")
def complete():
    """Survey is complete"""
    # survey_id = session[CURRENT_SURVEY_KEY]
    # survey = surveys[survey_id]
    responses = session[RESPONSES_KEY]

    return render_template("complete.html", survey=survey, responses=responses)
