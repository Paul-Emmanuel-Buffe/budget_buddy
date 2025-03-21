from flask import Flask, request, redirect, url_for, render_template, session, flash
from markupsafe import escape
from user import User
import hashlib
import secrets
from datetime import timedelta
import pandas as pd
from compte import Account
from type import Type
from category import Category
from datetime import date
from transaction import Transaction

app = Flask(__name__)
app.secret_key = 'aloha'
app.permanent_session_lifetime = timedelta(minutes=60)
user = User()
account = Account()
type = Type()
categorie = Category()
transac = Transaction()

@app.route('/simuler_connexion')
def simuler_connexion():
    # Simuler une connexion en définissant les clés nécessaires dans la session
    session['user'] = 'utilisateur_test'  # Nom d'utilisateur simulé
    session['idUtilisateur'] = 3  # ID utilisateur simulé (remplacez par une valeur valide)
    session.permanent = True  # Rendre la session permanente

    # Message de confirmation
    flash('Connexion simulée avec succès. Vous pouvez maintenant accéder aux fonctionnalités.', 'success')
    return redirect(url_for('index'))

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

    try:
        # S'assurer que la connexion est active
        user.ensure_connection()
        
        # Requête SQL pour récupérer les transactions
        query = '''
            SELECT description, montant, dateTransaction 
            FROM transaction 
            WHERE idCompte = %s 
            ORDER BY dateTransaction DESC
        '''
        
        user.cursor.execute(query, (3,))
        results = user.cursor.fetchall()
        
        # Obtenez les noms des colonnes - ajustez selon votre version de MySQL
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
    
    except Exception as e:
        # Gestion des erreurs
        return f"Une erreur s'est produite : {str(e)}", 500

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



@app.route('/traitementTransaction', methods=["POST"])
def traitementTransaction():
    if request.method == "POST":
            
            compte = request.form.get('compte')
            compteVir = request.form['comptevirement']
            description = request.form['description']
            descriptionvir = request.form['descriptionvir']
            montant = float(request.form['montant'])
            categorie = request.form['category']
            type = request.form['type']
            dateTrans = date.today()

            print(compte)
            accounts = account.readAccounts(session['idUtilisateur'], compte)
            accountver = account.readAccounts(session['idUtilisateur'], compteVir)

            if type == '1':
                calculRetrait = accounts[0]['montant'] - montant
                transac.create(description, montant, dateTrans, categorie, type, compte)
                account.update(calculRetrait, compte)
            elif type == '2':
                calculvers = accounts[0]['montant'] + montant
                transac.create(description, montant, dateTrans, categorie, type, compte)
                account.update(calculvers, compte)
            elif type == '3':
                calculRetrait = accounts[0]['montant'] - montant
                transac.create(description, montant, dateTrans, categorie, type, compte)
                account.update(calculRetrait, compte)

                calculvers = accountver[0]['montant'] + montant
                transac.create(descriptionvir, montant, dateTrans, categorie, type, compteVir)
                account.update(calculvers, compteVir)
                

            

            return redirect(url_for('doTransactions'))

@app.route("/actions")
def actions():
    return render_template('actions.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.clear()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))

@app.route('/listAccount')
def listAccount():
    Data = account.read(session['idUtilisateur'])
    return render_template('listAccount.html', data=Data)

@app.route('/doTransaction')
def doTransactions():

    ## date = annee mois jour ##
    eType = type.read()
    eCategorie = categorie.read()
    listAc = account.read(session['idUtilisateur'])
    return render_template('doTransaction.html', account=listAc, categorie=eCategorie, type=eType)


@app.route("/synthese")
def synthese():
    return render_template('synthese.html')




@app.route('/display_filter')
def display_filter():
    # Vérifie si l'utilisateur est connecté
    if 'user' not in session:
        return redirect(url_for('index'))

    # S'assurer que la connexion est active
    user.ensure_connection()

    # Récupérer les paramètres de la requête
    date = request.args.get('date')
    categorie = request.args.get('categorie')
    type_transaction = request.args.get('type')
    tri_montant = request.args.get('tri_montant')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')

    # Construction de la requête SQL avec jointures pour afficher plus d'infos
    query = """
        SELECT t.reference, t.description, t.montant, t.dateTransaction, 
               c.titre AS categorie, ty.titre AS type_transaction
        FROM transaction t
        LEFT JOIN categorie c ON t.idCategorie = c.idCategorie
        LEFT JOIN type ty ON t.idType = ty.idType
        WHERE t.idCompte = %s
    """
    params = [session['idUtilisateur']]

    # Ajout des filtres à la requête si nécessaire
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

    # Ajout du tri si demandé, sinon tri par date décroissante
    if tri_montant:
        query += f" ORDER BY t.montant {'ASC' if tri_montant == 'croissant' else 'DESC'}"
    else:
        query += " ORDER BY t.dateTransaction DESC"

    # Débogage : afficher la requête et les paramètres
    print(f"Executing query: {query}")
    print(f"With params: {params}")

    try:
        # Exécuter la requête SQL
        user.cursor.execute(query, tuple(params))
        results = user.cursor.fetchall()

        # Récupérer dynamiquement les noms des colonnes
        columns = [desc[0] for desc in user.cursor.description]

        # Création du DataFrame pandas pour un affichage dynamique
        df = pd.DataFrame(results, columns=columns)

        # Conversion du DataFrame en HTML (avec classes Bootstrap pour le style)
        df_html = df.to_html(classes='table table-striped table-bordered', index=False)

        return render_template('dislay_filter.html', table=df_html)

    except Exception as e:
        print(f"Database error: {e}")
        return "Une erreur est survenue lors du chargement des données.", 500 




if __name__ == '__main__':
    app.run(debug=True)
