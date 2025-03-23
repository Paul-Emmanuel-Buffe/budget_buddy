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

        query = 'insert into compte (montant, idUtilisateur) values (%s,%s);'
        self.cursor.execute(query, (montant, idUtilisateur))
        self.myDb.commit()

    
    def read(self, utilisateur):
        print('utilisateur : ', utilisateur)
        query = 'select * from compte where idUtilisateur = %s'
        self.cursor.execute(query, (utilisateur, ))
        accounts = []
        for i in self.cursor:
            account = {
                'accountNumber':i[0],
                'montant':i[1],
                'nom_utilisateur':i[2],
                }
            accounts.append(account)
        return accounts
    
    def readAccounts(self, utilisateur, compte):
        print('utilisateur : ', utilisateur)
        query = 'select * from compte where idUtilisateur = %s and idCompte = %s'
        self.cursor.execute(query, (utilisateur, compte))
        accountsUser = []
        for i in self.cursor:
            accountUser = {
                'accountNumber':i[0],
                'montant':i[1],
                'nom_utilisateur':i[2],
                }
            accountsUser.append(accountUser)
        return accountsUser
        
    def update(self, montant, compte):
        query = 'update compte set montant= %s where idCompte = %s'
        self.cursor.execute(query, (montant, compte))
        self.myDb.commit()

    def close_connection(self):
        self.cursor.close()
        self.myDb.close()