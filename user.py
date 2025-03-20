import mysql.connector

class User:
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
    
    def create(self, nom, prenom, email, motDePasse, salt, admin):
        self.ensure_connection()
        query = 'insert into utilisateur (nom, prenom, email, motDePasse, salt, admin) values (%s,%s,%s,%s,%s,%s);'
        self.cursor.execute(query, (nom, prenom, email, motDePasse, salt, admin))
        self.myDb.commit()
    
    def read(self):
        self.ensure_connection()
        self.cursor.execute('select nom,prenom,email from utilisateur;')
        users = []
        for i in self.cursor:
            user = {
                'nom': i[0],
                'prenom': i[1],
                'mail': i[2],
            }
            users.append(user)
        return users
    
    def read_connection(self, mail):
        self.ensure_connection()
        user = []
        query = 'select idUtilisateur, nom, email, motDePasse, salt from utilisateur where email = %s;'
        self.cursor.execute(query, (mail,))
        for i in self.cursor:
            for j, k in enumerate(i):
                user.append(k)
        return user
    
    def update(self, nom, prenom, email, id):
        self.ensure_connection()
        query = 'update utilisateur set nom = %s, prenom = %s, email = %s where idUtilisateur = %s'
        self.cursor.execute(query, (nom, prenom, email, id))
        self.myDb.commit()
    
    def close_connection(self):
        """Fermer proprement la connexion"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'myDb') and self.myDb:
                self.myDb.close()
        except:
            pass