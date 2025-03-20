from flask import Flask, request, redirect, url_for, render_template, session, flash
from markupsafe import escape
from user import User
import hashlib
import secrets
from datetime import timedelta
import pandas as pd
from compte import Account

app = Flask(__name__)
app.secret_key = 'aloha'
app.permanent_session_lifetime = timedelta(minutes=60)
user = User()
account = Account()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        nom = request.form.get('nom')
        motDePasse = request.form.get('motDePasse')

        if nom and motDePasse:
            user_record = user.query.filter_by(nom=nom).first()

            if user_record and user_record.check_password(motDePasse):
                return redirect(url_for('affichage_compte'))
            else:
                message = "No User"
        else:
            message = "Please fill in all fields"

    return render_template('index.html', message=message)

@app.route('/affichage_compte')
def affichage_compte():
    query = 'SELECT description, montant, dateTransaction FROM transaction WHERE idCompte = %s ORDER BY dateTransaction DESC'
    cursor.execute(query, (3,))  # Parameterize the query
    results = cursor.fetchall()

    columns = cursor.column_names

    df = pd.DataFrame(results, columns=columns)
    df.rename(columns={'description': 'Opérations', 'montant': 'Montant', 'dateTransaction': 'Date'}, inplace=True)
    df_html = df.to_html(classes='table table-striped', index=False)

    return render_template('affichage_compte.html', table=df_html)

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
        user.create(nom, prenom, email, hash_hex, salt, admin)
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
            session['idUtilisateur'] = infoUtilisateur[0]
            session.permanent = True
            flash('Vous vous êtes connecté avec succès', 'success')
            return redirect(url_for('index'))
        else:
            flash('Le mail ou le mot de passe ne sont pas corrects')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
