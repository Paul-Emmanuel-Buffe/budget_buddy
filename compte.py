import mysql.connector

class Account:
    def __init__(self):
        self.myDb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cN06+#P34",
            database="banque",
            port=3306
        )
        self.cursor = self.myDb.cursor()

    def create(self, montant, idUtilisateur):
        # Crée un nouveau compte
        query = 'INSERT INTO compte (montant, idUtilisateur) VALUES (%s, %s);'
        self.cursor.execute(query, (montant, idUtilisateur))
        self.myDb.commit()

    def read(self, utilisateur):
        # Récupère tous les comptes d'un utilisateur
        query = 'SELECT * FROM compte WHERE idUtilisateur = %s'
        self.cursor.execute(query, (utilisateur,))
        accounts = []
        for i in self.cursor:
            account = {
                'accountNumber': i[0],
                'montant': i[1],
                'nom_utilisateur': i[2],
            }
            accounts.append(account)
        return accounts
    
    def readAccounts(self, utilisateur, compte):
        # Récupère un compte spécifique d'un utilisateur
        query = 'SELECT * FROM compte WHERE idUtilisateur = %s AND idCompte = %s'
        self.cursor.execute(query, (utilisateur, compte))
        accountsUser = []
        for i in self.cursor:
            accountUser = {
                'accountNumber': i[0],
                'montant': i[1],
                'nom_utilisateur': i[2],
            }
            accountsUser.append(accountUser)
        return accountsUser
        
    def update(self, montant, compte):
        # Met à jour le montant d'un compte
        query = 'UPDATE compte SET montant = %s WHERE idCompte = %s'
        self.cursor.execute(query, (montant, compte))
        self.myDb.commit()

    def close_connection(self):
        # Ferme les connexions à la base de données
        self.cursor.close()
        self.myDb.close()