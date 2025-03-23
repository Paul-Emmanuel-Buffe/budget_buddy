import mysql.connector

class Type:
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
            # Vérifier si la connexion est active avec une requête simple
            self.cursor.execute("SELECT 1")
            self.cursor.fetchone()
        except:
            # Reconnecter si la connexion est perdue
            self.connect_db()
       
    def read(self):
        self.ensure_connection()
        self.cursor.execute('select idType, titre from type;')
        types = []
        for i in self.cursor:
            type = {
                'idType': i[0],
                'titre': i[1],
            }
            types.append(type)
        return types
    
    def close_connection(self):
        """Fermer proprement la connexion"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'myDb') and self.myDb:
                self.myDb.close()
        except:
            pass