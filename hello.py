from flask import *
from markupsafe import *
from user import User
import hashlib
import secrets
from time import *
from datetime import *
from compte import Account


app = Flask(__name__)
app.secret_key = 'aloha'
app.permanent_session_lifetime = timedelta(minutes=60)
user = User()
account = Account()

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerAccount")
def registerAccount():
    return render_template("registerAccount.html")

@app.route('/action')
def action():
    return render_template('action.html')

@app.route('/traitementregisterAccount', methods=["POST"])
def traitementregisterAccount():
    
    if request.method == "POST":
        montant = request.form['montant']
        account.create(montant, session['idUtilisateur'])
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

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

        return redirect(url_for('index'))
    
@app.route('/traitementConnexion', methods=["POST"])
def traitementConnexion():
    
    if request.method == "POST":
        email = request.form['email']
        infoUtilisateur = user.read_connection(email)
        password = request.form['password']
        
        mdpHacher = hashlib.sha256((password + infoUtilisateur[4]).encode())
        hash_hex = mdpHacher.hexdigest()


        if email == infoUtilisateur[2] and hash_hex == infoUtilisateur[3]:
            session['user'] = infoUtilisateur[1]
            session['idUtilisateur']= infoUtilisateur[0]
            session.permanent = True
            flash('vous vous etes connecté avec succés', 'success')
            return redirect(url_for('index'))
        else:
            flash('le mail ou le mot de passe ne sont pas correcte')
    else:
        return redirect(url_for('index'))
    

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))