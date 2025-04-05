# Models/Utilisateur.py
import bcrypt
from Database.mongodb import MongoDB
from Database.redisdb import RedisDB


class Utilisateur:
    """
    Classe représentant un utilisateur avec les attributs suivants:
    - nom
    - prenom
    - telephone
    - email
    - mot_de_passe
    - role
    """

    ROLES = ["admin", "enseignant", "etudiant"]

    def __init__(self, nom, prenom, telephone, email, mot_de_passe, role="etudiant"):
        """
        Initialise un nouvel utilisateur avec les attributs fournis.

        Args:
            nom (str): Nom de l'utilisateur
            prenom (str): Prénom de l'utilisateur
            telephone (str): Numéro de téléphone
            email (str): Adresse email
            mot_de_passe (str): Mot de passe
            role (str): Rôle de l'utilisateur (admin, enseignant, etudiant)
        """
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.email = email
        self.mot_de_passe = mot_de_passe

        # Vérifier si le rôle est valide
        if role in self.ROLES:
            self.role = role
        else:
            self.role = "etudiant"  # Par défaut

    def afficher_infos(self):
        """Affiche les informations de l'utilisateur (sans le mot de passe)"""
        return f"Utilisateur: {self.prenom} {self.nom}\nTéléphone: {self.telephone}\nEmail: {self.email}\nRôle: {self.role}"

    def modifier_telephone(self, nouveau_telephone):
        """
        Modifie le numéro de téléphone de l'utilisateur.

        Args:
            nouveau_telephone (str): Nouveau numéro de téléphone
        """
        self.telephone = nouveau_telephone

    def modifier_mot_de_passe(self, ancien_mot_de_passe, nouveau_mot_de_passe):
        """
        Modifie le mot de passe de l'utilisateur.

        Args:
            ancien_mot_de_passe (str): Mot de passe actuel (pour vérification)
            nouveau_mot_de_passe (str): Nouveau mot de passe

        Returns:
            bool: True si la modification est réussie, False sinon
        """
        # ATTENTION: Cette méthode ne fonctionne pas correctement avec des mots de passe hachés
        # Dans un système réel, il faudrait vérifier avec bcrypt.checkpw et hacher le nouveau mot de passe
        # Cette méthode est à utiliser uniquement dans la console, pas dans le repository
        if self.mot_de_passe == ancien_mot_de_passe:
            self.mot_de_passe = nouveau_mot_de_passe
            return True
        return False

    def to_dict(self):
        """
        Convertit l'utilisateur en dictionnaire pour MongoDB

        Returns:
            dict: Dictionnaire représentant l'utilisateur
        """
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "telephone": self.telephone,
            "email": self.email,
            "mot_de_passe": self.mot_de_passe,
            "role": self.role
        }

    @staticmethod
    def from_dict(data):
        """
        Crée un utilisateur à partir d'un dictionnaire

        Args:
            data (dict): Dictionnaire représentant un utilisateur

        Returns:
            Utilisateur: Nouvelle instance d'utilisateur
        """
        return Utilisateur(
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            telephone=data.get("telephone"),
            email=data.get("email"),
            mot_de_passe=data.get("mot_de_passe"),
            role=data.get("role", "etudiant")
        )