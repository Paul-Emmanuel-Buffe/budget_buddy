import mysql.connector

class Account:
    def __init__(self):
        self.myDb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="banque"
        )
        self.cursor = self.myDb.cursor(buffered=True)

    def create(self, montant, idUtilisateur):

        query = 'insert into compte (montant, idUtilisateur) values (%s,%s);'
        self.cursor.execute(query, (montant, idUtilisateur))
        self.myDb.commit()

    
    def read(self, utilisateur):
        query = ' select utilisateur.nom, utilisateur.prenom, compte.idCompte as numeroDeCompte, montant from compte inner join utilisateur on utilisateur.idUtilisateur = compte.idUtilisateur where utilisateur.idUtilisateur = %s order by idCompte asc; '
        self.cursor.execute(query, (utilisateur,))
        result = self.cursor.fetchall()
        accounts = []
        for results in result:
            account = {
                'nom':results[0],
                'prenom':results[1],
                'numeroDeCompte':results[2],
                'montant':results[3]
                }
            accounts.append(account)
            print(accounts)
        return accounts
            
        
    def update(self, montant):
        query = 'update compte set montant= %s where id = %s'
        self.cursor.execute(query, (montant))
        self.myDb.commit()

    def close_connection(self):
        self.cursor.close()
        self.myDb.close()
