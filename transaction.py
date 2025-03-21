import mysql.connector

class Transaction:
    def __init__(self):
        self.connect_db()
    
    def connect_db(self):
        """Établir ou rétablir la connexion à la base de données"""
        try:
            # Fermer la connexion existante si elle existe
            if hasattr(self, 'myDb') and self.myDb:
                try:
                    self.cursor.close()
                    self.myDb.close()
                except:
                    pass
            
            # Créer une nouvelle connexion
            self.myDb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="banque",
                port=3306
            )
            self.cursor = self.myDb.cursor()
        except mysql.connector.Error as err:
            print(f"Erreur de connexion à la base de données: {err}")
            raise
    
    def ensure_connection(self):
        """S'assurer que la connexion est active"""
        try:
            # Vérifier si la connexion est active avec une requête simple
            self.cursor.execute("SELECT 1")
            self.cursor.fetchone()
        except:
            # Reconnecter si la connexion est perdue
            self.connect_db()
    
    def create(self,description, montant, dateTransaction, idCategorie, idType, idCompte):
        self.ensure_connection()
        query = 'insert into transaction (description, montant, dateTransaction, idCategorie, idType, idCompte) values (%s,%s,%s,%s,%s,%s);'
        self.cursor.execute(query, (description, montant, dateTransaction, idCategorie, idType, idCompte))
        self.myDb.commit()
    
    def read(self, compte):
        self.ensure_connection()
        query = 'select * from transactions where idCompte = %s'
        self.cursor.execute(query, (compte,))
        transactions = []
        for i in self.cursor:
            transaction = {
                'reference': i[0],
                'description': i[1],
                'montant': i[2],
                'dateTransaction': i[3],
                'idCategorie': i[4],
                'idType': i[5],
            }
            transactions.append(transaction)
        return transactions
    
    
        

    def close_connection(self):
        """Fermer proprement la connexion"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'myDb') and self.myDb:
                self.myDb.close()
        except:
            pass