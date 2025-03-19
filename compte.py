import mysql.connector

class User:
    def __init__(self):
        self.myDb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="banque"
        )
        self.cursor = self.myDb.cursor()

    def create(self, montant, idUtilisateur):

        query = 'insert into utilisateur (montant, idUtilisateur) values (%s,%s);'
        self.cursor.execute(query, (montant, idUtilisateur))
        self.myDb.commit()

    
    def read(self):
        self.cursor.execute('select * from compte;')
        for i in self.cursor:
            account = {
                'accountNumber':i[0],
                'montant':i[1],
                'nom_utilisateur':i[2],
                }
            
        
    def update(self, montant):
        query = 'update compte set montant= %s where id = %s'
        self.cursor.execute(query, (montant))
        self.myDb.commit()

    def close_connection(self):
        self.cursor.close()
        self.myDb.close()
