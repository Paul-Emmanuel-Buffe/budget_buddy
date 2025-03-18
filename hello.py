from flask import *
from markupsafe import escape
from utilisateur import Utilisateur

app = Flask(__name__)

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/connection")
def connection():
    return render_template("connection.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/action')
def action():
    return render_template('action.html')