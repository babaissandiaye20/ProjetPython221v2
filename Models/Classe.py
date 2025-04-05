class Classe:
    """
    Classe représentant une classe d'étudiants
    """

    def __init__(self, nom, niveau, annee_scolaire, matieres=None):
        """
        Initialise une nouvelle classe

        Args:
            nom (str): Nom de la classe (ex: 'Terminale S')
            niveau (str): Niveau d'études (ex: 'Lycée')
            annee_scolaire (str): Année scolaire (ex: '2024-2025')
            matieres (list): Liste des matières enseignées
        """
        self.nom = nom
        self.niveau = niveau
        self.annee_scolaire = annee_scolaire
        self.matieres = matieres if matieres else []

    def ajouter_matiere(self, matiere):
        """
        Ajoute une matière à la classe

        Args:
            matiere (str): Nom de la matière
        """
        if matiere not in self.matieres:
            self.matieres.append(matiere)

    def supprimer_matiere(self, matiere):
        """
        Supprime une matière de la classe

        Args:
            matiere (str): Nom de la matière

        Returns:
            bool: True si la matière a été supprimée, False sinon
        """
        if matiere in self.matieres:
            self.matieres.remove(matiere)
            return True
        return False

    def to_dict(self):
        """
        Convertit la classe en dictionnaire pour MongoDB

        Returns:
            dict: Dictionnaire représentant la classe
        """
        return {
            "nom": self.nom,
            "niveau": self.niveau,
            "annee_scolaire": self.annee_scolaire,
            "matieres": self.matieres
        }

    @staticmethod
    def from_dict(data):
        """
        Crée une classe à partir d'un dictionnaire

        Args:
            data (dict): Dictionnaire représentant une classe

        Returns:
            Classe: Nouvelle instance de classe
        """
        return Classe(
            nom=data.get("nom"),
            niveau=data.get("niveau"),
            annee_scolaire=data.get("annee_scolaire"),
            matieres=data.get("matieres", [])
        )