class Etudiant:
    """
    Classe représentant un étudiant avec les attributs suivants:
    - nom
    - prenom
    - telephone
    - email
    - classe
    - notes (dictionnaire matière:note)
    """

    def __init__(self, nom, prenom, telephone, email, classe=None, notes=None):
        """
        Initialise un nouvel étudiant avec les attributs fournis.

        Args:
            nom (str): Nom de l'étudiant
            prenom (str): Prénom de l'étudiant
            telephone (str): Numéro de téléphone
            email (str): Adresse email
            classe (str): Classe de l'étudiant
            notes (dict): Dictionnaire des notes par matière
        """
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.email = email
        self.classe = classe
        self.notes = notes if notes else {}

    def calculer_moyenne(self):
        """Calcule la moyenne générale de l'étudiant"""
        if not self.notes:
            return 0

        total = sum(self.notes.values())
        return round(total / len(self.notes), 2)

    def ajouter_note(self, matiere, note):
        """
        Ajoute ou modifie une note pour une matière

        Args:
            matiere (str): Nom de la matière
            note (float): Note entre 0 et 20

        Returns:
            bool: True si la note est valide, False sinon
        """
        if 0 <= note <= 20:
            self.notes[matiere] = note
            return True
        return False

    def supprimer_note(self, matiere):
        """
        Supprime une note pour une matière

        Args:
            matiere (str): Nom de la matière

        Returns:
            bool: True si la matière existait, False sinon
        """
        if matiere in self.notes:
            del self.notes[matiere]
            return True
        return False

    def afficher_infos(self):
        """Affiche les informations de l'étudiant"""
        info = f"Étudiant: {self.prenom} {self.nom}\n"
        info += f"Téléphone: {self.telephone}\n"
        info += f"Email: {self.email}\n"
        info += f"Classe: {self.classe or 'Non assignée'}\n"
        info += f"Moyenne générale: {self.calculer_moyenne()}/20\n"

        if self.notes:
            info += "Notes:\n"
            for matiere, note in self.notes.items():
                info += f"  - {matiere}: {note}/20\n"
        else:
            info += "Aucune note enregistrée.\n"

        return info

    def to_dict(self):
        """
        Convertit l'étudiant en dictionnaire pour MongoDB

        Returns:
            dict: Dictionnaire représentant l'étudiant
        """
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "telephone": self.telephone,
            "email": self.email,
            "classe": self.classe,
            "notes": self.notes
        }

    @staticmethod
    def from_dict(data):
        """
        Crée un étudiant à partir d'un dictionnaire

        Args:
            data (dict): Dictionnaire représentant un étudiant

        Returns:
            Etudiant: Nouvelle instance d'étudiant
        """
        return Etudiant(
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            telephone=data.get("telephone"),
            email=data.get("email"),
            classe=data.get("classe"),
            notes=data.get("notes", {})
        )