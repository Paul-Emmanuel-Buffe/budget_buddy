import matplotlib.pyplot as plt
import io
import base64
from matplotlib.figure import Figure
from datetime import datetime

class GraphManager:
    """
    Classe pour gérer la création et la génération de graphiques
    pour l'application de gestion financière.
    """

    def __init__(self):
        """Initialisation du gestionnaire de graphiques."""
        pass

    def generate_pie_chart(self, categories, montants, titre="Répartition des dépenses"):
        """
        Génère un graphique en camembert à partir des catégories et montants fournis.
        
        Args:
            categories (list): Liste des noms de catégories à afficher
            montants (list): Liste des montants correspondant aux catégories
            titre (str): Titre du graphique
            
        Returns:
            str: Image encodée en base64 au format data URI
        """
        # Création de la figure
        fig = Figure(figsize=(30, 25))
        ax = fig.add_subplot(111)

        # Tailles de la police
        title_font_size = 100
        label_font_size = 80
        autopct_font_size = 70

        # Création du camembert
        wedges, texts, autotexts = ax.pie(
            montants,
            labels=categories,
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            textprops={'fontsize': autopct_font_size}  # Taille de la police pour les pourcentages
        )

        # Taille de la police pour les étiquettes
        plt.setp(texts, size=label_font_size)

        # Titre avec une taille de police spécifiée
        ax.set_title(titre, fontsize=title_font_size)

        # Égalisation des axes
        ax.axis('equal')

        # Enregistrement de l'image dans un buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        # Encodage de l'image en base64
        img_data = base64.b64encode(buf.getbuffer()).decode("utf-8")

        return f"data:image/png;base64,{img_data}"

    def get_expense(self, user, user_id, start_date=None, end_date=None):
        """
        Récupère les données de dépenses depuis la BDD et génère un graphique en camembert.
        
        Args:
            user (User): Objet utilisateur contenant la connexion à la BDD
            user_id (int): ID de l'utilisateur dont on veut afficher les dépenses
            start_date (datetime, optional): Date de début pour filtrer les transactions
            end_date (datetime, optional): Date de fin pour filtrer les transactions
            
        Returns:
            str: Image du graphique en camembert encodée en base64
        """
        try:
            query = """
                SELECT c.titre, SUM(t.montant) as total
                FROM transaction t
                JOIN categorie c ON t.idCategorie = c.idCategorie
                JOIN compte cpt ON t.idCompte = cpt.idCompte
                WHERE cpt.idUtilisateur = %s AND t.idType = 2
            """

            # Ajout de la condition de date si les dates sont fournies
            if start_date and end_date:
                query += " AND t.dateTransaction BETWEEN %s AND %s"
                params = (user_id, start_date, end_date)
            else:
                params = (user_id,)

            query += " GROUP BY c.titre"

            # Exécution de la requête
            user.cursor.execute(query, params)
            results = user.cursor.fetchall()

            if not results:
                return self.generate_pie_chart(["Aucune donnée"], [1], "Pas de dépenses à afficher")

            # Extraction des catégories et montants
            categories = [row[0] for row in results]
            montants = [abs(float(row[1])) for row in results]  # Conversion en valeurs absolues

            # Génération du graphique
            return self.generate_pie_chart(categories, montants, "Répartition des dépenses")
        except Exception as e:
            print(f"Erreur lors de la génération du graphique: {e}")
            return self.generate_pie_chart(["Erreur"], [1], "Erreur lors de la récupération des données")