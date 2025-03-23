import matplotlib.pyplot as plt
import io
import base64
from matplotlib.figure import Figure
from datetime import datetime

class GraphManager:
    """Classe pour gérer la création et la génération de graphiques."""
    
    def __init__(self):
        pass
    
    def generate_pie_chart(self, categories, montants):
        """Génère un graphique en camembert."""
        fig = Figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        label_font_size = 28
        autopct_font_size = 25
        
        wedges, texts, autotexts = ax.pie(
            montants,
            labels=categories,
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            textprops={'fontsize': autopct_font_size}
        )
        
        plt.setp(texts, size=label_font_size)
        ax.axis('equal')
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        
        img_data = base64.b64encode(buf.getbuffer()).decode("utf-8")
        
        return f"data:image/png;base64,{img_data}"
    
    def get_expense(self, user, user_id, start_date=None, end_date=None):
        """Récupère les dépenses et génère un graphique."""
        try:
            query = """
                SELECT c.titre, SUM(t.montant) as total
                FROM transaction t
                JOIN categorie c ON t.idCategorie = c.idCategorie
                JOIN compte cpt ON t.idCompte = cpt.idCompte
                WHERE cpt.idUtilisateur = %s AND t.idType = 2
            """
            
            if start_date and end_date:
                query += " AND t.dateTransaction BETWEEN %s AND %s"
                params = (user_id, start_date, end_date)
            else:
                params = (user_id,)
            
            query += " GROUP BY c.titre"
            
            user.cursor.execute(query, params)
            results = user.cursor.fetchall()
            
            if not results:
                return self.generate_pie_chart(["Aucune donnée"], [1])
            
            categories = [row[0] for row in results]
            montants = [abs(float(row[1])) for row in results]
            
            return self.generate_pie_chart(categories, montants)
        except Exception as e:
            print(f"Erreur lors de la génération du graphique: {e}")
            return self.generate_pie_chart(["Erreur"], [1])