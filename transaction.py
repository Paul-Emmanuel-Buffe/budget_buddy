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
                password="cN06+#P34",
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
            self.cursor.execute("SELECT 1")
            self.cursor.fetchone()
        except:
            self.connect_db()
    
    def create(self, description, montant, dateTransaction, idCategorie, idType, idCompte):
        """Créer une nouvelle transaction"""
        self.ensure_connection()
        query = 'INSERT INTO transaction (description, montant, dateTransaction, idCategorie, idType, idCompte) VALUES (%s, %s, %s, %s, %s, %s);'
        self.cursor.execute(query, (description, montant, dateTransaction, idCategorie, idType, idCompte))
        self.myDb.commit()
    
    def read(self, compte):
        """Lire les transactions d'un compte"""
        self.ensure_connection()
        query = 'SELECT * FROM transactions WHERE idCompte = %s'
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