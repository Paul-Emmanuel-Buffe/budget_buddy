from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:cN06+#P34@localhost/banque' # Remplacer selon l'architecture 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle de la table Utilisateur
class User(db.Model):
    __tablename__ = 'Utilisateur'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=True)
    motDePasse = db.Column(db.String(255), nullable=True)

    def check_password(self, password):
        return check_password_hash(self.motDePasse, password)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        motDePasse = request.form['motDePasse']
        user = User.query.filter_by(username=username, motDePasse=motDePasse).first()
        if user and user.check_password(motDePasse):
            message = "User ready"
        else:
            message = "No User"
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
