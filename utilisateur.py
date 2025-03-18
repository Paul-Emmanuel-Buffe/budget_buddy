import mysql.connector

class Utilisateur:
    def __init__(self):
        self.myDb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="store"
        )
        self.cursor = self.myDb.cursor()

    def create(self, nom, prenom, email, motDePasse):

        query = 'insert into utilisateur (nom, prenom, email, motDePasse,admin) values (%s,%s,%s,%s,%s);'
        self.cursor.execute(query, ( nom, prenom, email, motDePasse))
        self.myDb.commit()

    
    def read(self):
        self.cursor.execute('select idUtilisateur, nom,prenom,email from utilisateur;')
        for i in self.cursor:
            product = {
                'id':i[0],
                'nom':i[1],
                'prenom':i[2],
                'mail':i[3],
                }
            
        
    def update(self, nom,description,price,quantity, id):
        query = 'update product set nom = %s , prenom = %s , email = %s where id = %s'
        self.cursor.execute(query, (nom,description,price,quantity, id))
        self.myDb.commit()

    def close_connection(self):
        self.cursor.close()
        self.myDb.close()
