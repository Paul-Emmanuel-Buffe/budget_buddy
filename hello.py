from flask import *
from markupsafe import escape
from user import User
import hashlib
import secrets

app = Flask(__name__)
user = User()

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/action')
def action():
    return render_template('action.html')

@app.route('/traitement', methods=["POST"])
def traitement():
    if request.method == "POST":
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']

        password = request.form['password']
        salt = secrets.token_hex(16)
        mdpHacher = hashlib.sha256((password + salt).encode())
        hash_hex = mdpHacher.hexdigest()

        admin = False

        user.create(nom, prenom, email, hash_hex ,salt,admin)

        return redirect(url_for('/index'))
    
@app.route('/traitementConnexion', methods=["POST"])
def traitementConnexion():
    
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        listUtilisateur = user.read_connection(email)
        
        print(user.listeUser)

        return redirect(url_for('index'))
    
    else:
        return redirect(url_for('index'))
    
