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
        self.listeUser = []
    
    def create(self, nom, prenom, email, motDePasse, salt, admin):

        query = 'insert into utilisateur (nom, prenom, email, motDePasse, salt, admin) values (%s,%s,%s,%s,%s,%s);'
        self.cursor.execute(query, ( nom, prenom, email, motDePasse,salt, admin))
        self.myDb.commit()

    
    def read(self):
        self.cursor.execute('select nom,prenom,email from utilisateur;')
        for i in self.cursor:
            user = {
                'id':i[0],
                'nom':i[1],
                'prenom':i[2],
                'mail':i[3],
                }
            
            
    def read_connection(self, mail):
        query = 'select email, motDePasse, salt from utilisateur where email = %s;'

        self.cursor.execute(query, (mail,))

        for i in self.cursor:
            print(i)
            user = {
                'mail':i[0],
                'motDePasse':i[1],
                'salt':i[2]
                }
            self.listeUser.append(user)
            
        
    def update(self, nom,description,price,quantity, id):
        query = 'update product set nom = %s , prenom = %s , email = %s where id = %s'
        self.cursor.execute(query, (nom,description,price,quantity, id))
        self.myDb.commit()

    def close_connection(self):
        self.cursor.close()
        self.myDb.close()
