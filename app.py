from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolBarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SSECRET_KEY'] = "oh so secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolBarExtension(app)


@app.route('/')
def index():
    """Return homepage."""

    return render_template("start.html")
