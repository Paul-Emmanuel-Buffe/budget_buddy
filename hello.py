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
    # Vérifiez si l'utilisateur est connecté
    if 'user' not in session:
        return redirect(url_for('index'))

    else:
        # S'assurer que la connexion est active
        user.ensure_connection()

        # Récupérer les paramètres de la requête
        date = request.args.get('date')
        categorie = request.args.get('categorie')
        type_transaction = request.args.get('type')
        tri_montant = request.args.get('tri_montant')
        date_debut = request.args.get('date_debut')
        date_fin = request.args.get('date_fin')

        # Construire la requête SQL en fonction des filtres
        query = "SELECT description, montant, dateTransaction FROM transaction WHERE idCompte = %s"
        params = [session['idUtilisateur'],]

        # Ajouter des filtres à la requête si nécessaire
        if date:  # Si une date spécifique est fournie
            query += " AND dateTransaction = %s"
            params.append(date)

        if categorie:  # Si une catégorie est fournie
            query += " AND idCategorie = %s"
            params.append(categorie)

        if type_transaction:  # Si un type de transaction est fourni
            query += " AND idType = %s"
            params.append(type_transaction)

        if date_debut and date_fin:  # Si une plage de dates est fournie
            query += " AND dateTransaction BETWEEN %s AND %s"
            params.extend([date_debut, date_fin])

        if tri_montant:  # Si un tri sur le montant est demandé
            query += f" ORDER BY montant {'ASC' if tri_montant == 'croissant' else 'DESC'}"
        else:
            query += " ORDER BY dateTransaction DESC"

        # Débogage : afficher la requête et les paramètres
        print(f"Executing query: {query}")
        print(f"With params: {params}")

        # Exécuter la requête SQL
    try:
        user.cursor.execute(query, params)
        results = user.cursor.fetchall()
    except Exception as e:
        print(f"Database error: {e}")
        return "An error occurred while fetching data.", 500
        # Obtenez les noms des colonnes
    columns = [desc[0] for desc in user.cursor.description]


        # Création d'un DataFrame pandas pour formater les données
    df = pd.DataFrame(results, columns=columns)
    df.rename(columns={
            'description': 'Opérations',
            'montant': 'Montant',
            'dateTransaction': 'Date'
        }, inplace=True)

        # Conversion du DataFrame en HTML
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

@app.route('/synthese')
def synthese():
    # Vérifiez si l'utilisateur est connecté
    if 'user' not in session:
        return redirect(url_for('index'))

    try:
        # S'assurer que la connexion est active
        user.ensure_connection()

        # Récupérer les comptes de l'utilisateur
        query = "SELECT idCompte, montant FROM compte WHERE idUtilisateur = %s"
        params = (session['idUtilisateur'],)  # Tuple avec une virgule

        # Exécuter la requête SQL
        user.cursor.execute(query, params)
        results = user.cursor.fetchall()

        # Obtenir les noms des colonnes
        columns = [desc[0] for desc in user.cursor.description]

        # Création d'un DataFrame pandas pour formater les données
        df = pd.DataFrame(results, columns=columns)
        df.rename(columns={
            'idCompte': 'Numéro du Compte',
            'montant': 'Solde',
        }, inplace=True)

        # Calculer le total des soldes
        total_solde = df['Solde'].sum()

        # Ajouter une ligne pour le total
        total_row = pd.DataFrame({
            'Numéro du Compte': ['Total'],
            'Solde': [total_solde]
        })
        df = pd.concat([df, total_row], ignore_index=True)

        # Conversion du DataFrame en HTML
        df_html = df.to_html(classes='table table-striped', index=False)

        return render_template('synthese.html', table=df_html)

    except Exception as e:
        print(f"Erreur : {e}")
        return "Une erreur s'est produite lors de la récupération des données.", 500

    finally:
        # Fermer la connexion à la base de données
        user.close_connection()


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

@app.route("/actions")
def actions():
    return render_template('actions.html')



@app.route('/logout')
def logout():
    session.pop('user', None)
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))

@app.route('/doTransaction')
def doTransactions():
    return render_template('doTransaction.html')


















if __name__ == '__main__':
    app.run(debug=True)


















if __name__ == '__main__':
    app.run(debug=True)