from flask import Flask, request, redirect, url_for, render_template, session, flash
from markupsafe import escape
from user import User
import hashlib
import secrets
from datetime import timedelta, datetime, date
import pandas as pd
from compte import Account
from type import Type
from category import Category
from transaction import Transaction
from graph import GraphManager

app = Flask(__name__)
app.secret_key = 'aloha'
app.permanent_session_lifetime = timedelta(minutes=60)
user = User()
account = Account()
type = Type()
categorie = Category()
transac = Transaction()


@app.route('/', methods=['GET', 'POST'])
def index():
    """Page d'accueil avec authentification."""
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


@app.route('/traitementTransaction', methods=["POST"])
def traitementTransaction():
    """Traite les transactions (retrait, versement, virement)."""
    if request.method == "POST":
        compte = request.form.get('compte')
        compteVir = request.form['comptevirement']
        description = request.form['description']
        descriptionvir = request.form['descriptionvir']
        montant = float(request.form['montant'])
        categorie = request.form['category']
        type = request.form['type']
        dateTrans = date.today()

        accounts = account.readAccounts(session['idUtilisateur'], compte)
        accountver = account.readAccounts(session['idUtilisateur'], compteVir)

        if type == '1':  # Retrait
            calculRetrait = accounts[0]['montant'] - montant
            transac.create(description, montant, dateTrans, categorie, type, compte)
            account.update(calculRetrait, compte)
        elif type == '2':  # Versement
            calculvers = accounts[0]['montant'] + montant
            transac.create(description, montant, dateTrans, categorie, type, compte)
            account.update(calculvers, compte)
        elif type == '3':  # Virement
            # Débit du compte source
            calculRetrait = accounts[0]['montant'] - montant
            transac.create(description, montant, dateTrans, categorie, type, compte)
            account.update(calculRetrait, compte)

            # Crédit du compte destinataire
            calculvers = accountver[0]['montant'] + montant
            transac.create(descriptionvir, montant, dateTrans, categorie, type, compteVir)
            account.update(calculvers, compteVir)

        return redirect(url_for('doTransactions'))


@app.route('/affichage_compte')
def affichage_compte():
    """Affiche les détails du compte avec filtres."""
    if 'user' not in session:
        return redirect(url_for('index'))

    user.ensure_connection()

    # Récupérer les paramètres de filtrage
    date = request.args.get('date')
    categorie = request.args.get('categorie')
    type_transaction = request.args.get('type')
    tri_montant = request.args.get('tri_montant')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')

    # Construire la requête SQL avec filtres
    query = """
    SELECT t.idCompte, t.description, t.montant, t.dateTransaction, ty.titre AS type 
    FROM transaction t
    JOIN type ty ON t.idType = ty.idType
    WHERE t.idCompte IN (
        SELECT idCompte FROM compte WHERE idUtilisateur = %s
    )
    """
    params = [session['idUtilisateur']]

    if date:
        query += " AND t.dateTransaction = %s"
        params.append(date)

    if categorie:
        query += " AND t.idCategorie = %s"
        params.append(categorie)

    if type_transaction:
        query += " AND t.idType = %s"
        params.append(type_transaction)

    if date_debut and date_fin:
        query += " AND t.dateTransaction BETWEEN %s AND %s"
        params.extend([date_debut, date_fin])

    if tri_montant:
        query += f" ORDER BY t.montant {'ASC' if tri_montant == 'croissant' else 'DESC'}"
    else:
        query += " ORDER BY t.dateTransaction DESC"

    try:
        user.cursor.execute(query, params)
        results = user.cursor.fetchall()
        columns = [desc[0] for desc in user.cursor.description]

        # Création du DataFrame
        df = pd.DataFrame(results, columns=columns)
        df.rename(columns={
            'idCompte': 'Compte',
            'description': 'Opérations',
            'montant': 'Montant',
            'dateTransaction': 'Date',
            'type': 'Type'
        }, inplace=True)

        df_html = df.to_html(classes='table table-striped', index=False)
        return render_template('affichage_compte.html', table=df_html)
    except Exception as e:
        print(f"Database error: {e}")
        return "An error occurred while fetching data.", 500


@app.route("/register")
def register():
    """Page d'inscription."""
    return render_template("register.html")


@app.route("/registerAccount")
def registerAccount():
    """Page de création de compte bancaire."""
    return render_template("registerAccount.html")


@app.route('/action')
def action():
    """Page d'actions disponibles."""
    return render_template('action.html')


@app.route('/synthese', methods=['GET', 'POST'])
def synthese():
    """Page de synthèse avec graphiques et tableaux."""
    if 'user' not in session:
        return redirect(url_for('index'))

    try:
        user.ensure_connection()

        # Récupérer les dates de filtrage
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            start_date = None
            end_date = None

        # Récupérer les comptes
        query = "SELECT idCompte, montant FROM compte WHERE idUtilisateur = %s"
        params = (session['idUtilisateur'],)
        user.cursor.execute(query, params)
        results = user.cursor.fetchall()
        columns = [desc[0] for desc in user.cursor.description]

        # Créer le DataFrame
        df = pd.DataFrame(results, columns=columns)
        df.rename(columns={
            'idCompte': 'Numéro du Compte',
            'montant': 'Solde',
        }, inplace=True)

        # Calculer le total
        total_solde = df['Solde'].sum()
        total_row = pd.DataFrame({
            'Numéro du Compte': ['Total'],
            'Solde': [total_solde]
        })
        df = pd.concat([df, total_row], ignore_index=True)
        df_html = df.to_html(classes='table table-striped', index=False)

        # Générer le graphique
        graph_manager = GraphManager()
        user_id = session['idUtilisateur']
        pie_chart = graph_manager.get_expense(user, user_id, start_date, end_date)

        return render_template('synthese.html', table=df_html, pie_chart=pie_chart)

    except Exception as e:
        print(f"Erreur lors de la récupération des données: {e}")
        return "Une erreur est survenue lors de la récupération des données.", 500


@app.route('/traitementregisterAccount', methods=["POST"])
def traitementregisterAccount():
    """Traite la création d'un nouveau compte bancaire."""
    if request.method == "POST":
        montant = request.form['montant']
        account.create(montant, session['idUtilisateur'])
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/traitement', methods=["POST"])
def traitement():
    """Traite l'inscription d'un nouvel utilisateur."""
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
    """Traite la connexion d'un utilisateur."""
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
    """Page d'actions multiples."""
    return render_template('actions.html')


@app.route('/doTransaction')
def doTransactions():
    """Page pour effectuer une transaction."""
    eType = type.read()
    eCategorie = categorie.read()
    listAc = account.read(session['idUtilisateur'])
    return render_template('doTransaction.html', account=listAc, categorie=eCategorie, type=eType)


@app.route('/logout')
def logout():
    """Déconnexion de l'utilisateur."""
    session.pop('user', None)
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)