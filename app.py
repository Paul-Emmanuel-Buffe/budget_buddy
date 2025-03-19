from flask import Flask, render_template, request
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import pandas as pd


app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:cN06+#P34@localhost/banque'  # Remplacer selon l'architecture
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
connection =    {
    "user" : "root",
    "password" : "cN06+#P34",
    "host" : "localhost",
    "database" : "banque",
    "port" : 3306
    }
conn = mysql.connector.connect(**connection)

cursor = conn.cursor()

# Modèle de la table Utilisateur
class User(db.Model):
    __tablename__ = 'Utilisateur'
    idUtilisateur = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    motDePasse = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        nom = request.form.get('nom')  # Using .get() instead of direct indexing to prevent KeyError
        motDePasse = request.form.get('motDePasse')

        if nom and motDePasse:  # Make sure both fields are filled
            user = User.query.filter_by(nom=nom).first()  # Find user by 'nom'
            
            if user and user.check_password(motDePasse):  # Check password hash
                # Changement ici : redirection vers la page des comptes au lieu d'afficher un message
                return redirect(url_for('affichage_compte'))
            else:
                message = "No User"
        else:
            message = "Please fill in all fields"

    return render_template('index.html', message=message)

@app.route('/affichage_compte')
def affichage_compte():
    query= 'SELECT description, montant, dateTransaction FROM transaction WHERE idCompte = 3 ORDER by dateTransaction DESC'
    cursor.execute(query)
    results = cursor.fetchall()

    columns = cursor.column_names

    df = pd.DataFrame(results, columns=columns)
    df.rename(columns={'description': 'Opérations', 'montant': 'Montant', 'dateTransaction': 'Date'}, inplace=True)
    df_html = df.to_html(classes='table table-striped', index=False)

    return render_template('affichage_compte.html', table=df_html)

if __name__ == '__main__':
    app.run(debug=True)
