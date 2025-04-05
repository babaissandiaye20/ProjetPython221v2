# view/AuthConsole.py

from view.ConsoleManager import ConsoleManager
from Repositories.UtilisateurRepository import UtilisateurRepository
from Models.Utilisateur import Utilisateur
from view.AdminConsole import AdminConsole
from view.EnseignantConsole import EnseignantConsole
from view.EtudiantConsole import EtudiantConsole


class AuthConsole:
    """
    Console pour la gestion de l'authentification et de l'inscription
    """

    def __init__(self):
        self.user_repo = UtilisateurRepository()

    def afficher_menu_principal(self):
        """Affiche le menu principal de l'application"""
        while True:
            ConsoleManager.print_header("SYSTÈME DE GESTION DES ÉTUDIANTS")

            options = [
                (1, "Se connecter"),
                (2, "Créer un compte"),
                (3, "Quitter")
            ]

            ConsoleManager.print_menu(options)
            choice = ConsoleManager.get_user_choice(1, 3)

            if choice == 1:
                self.ecran_connexion()
            elif choice == 2:
                self.ecran_creation_compte()
            else:
                print("\nMerci d'avoir utilisé notre système. Au revoir!")
                break

    def ecran_connexion(self):
        """Affiche l'écran de connexion"""
        ConsoleManager.print_header("CONNEXION")

        email = input("Email: ")
        mot_de_passe = input("Mot de passe: ")

        # Authentifier l'utilisateur
        utilisateur, token = self.user_repo.authentifier(email, mot_de_passe)

        if utilisateur:
            ConsoleManager.print_message(f"Bienvenue, {utilisateur.prenom} {utilisateur.nom}!")
            ConsoleManager.print_message(f"Token de session: {token}")
            ConsoleManager.print_message(f"Rôle: {utilisateur.role}")

            # Rediriger vers la console appropriée selon le rôle
            if utilisateur.role == "admin":
                admin_console = AdminConsole(utilisateur)
                admin_console.afficher_menu_principal()
            elif utilisateur.role == "enseignant":
                enseignant_console = EnseignantConsole(utilisateur)
                enseignant_console.afficher_menu_principal()
            else:  # etudiant
                etudiant_console = EtudiantConsole(utilisateur)
                etudiant_console.afficher_menu_principal()
        else:
            ConsoleManager.print_message("Email ou mot de passe incorrect.", success=False)

    def ecran_creation_compte(self):
        """Affiche l'écran de création de compte"""
        ConsoleManager.print_header("CRÉATION DE COMPTE")

        nom = input("Nom: ")
        prenom = input("Prénom: ")
        telephone = input("Téléphone: ")
        email = input("Email: ")
        mot_de_passe = input("Mot de passe: ")

        # Demander le rôle (nouveau)
        ConsoleManager.print_message("Choisissez un rôle:")
        options = [
            (1, "Étudiant"),
            (2, "Enseignant"),
            (3, "Administrateur")
        ]
        ConsoleManager.print_menu(options)
        role_choice = ConsoleManager.get_user_choice(1, 3)

        # Convertir le choix en rôle
        roles = ["etudiant", "enseignant", "admin"]
        role = roles[role_choice - 1]

        # Créer l'utilisateur
        nouvel_utilisateur = Utilisateur(nom, prenom, telephone, email, mot_de_passe, role)

        # Créer l'utilisateur dans la base de données
        result = self.user_repo.creer_utilisateur(nouvel_utilisateur)

        if result:
            ConsoleManager.print_message(f"Compte créé avec succès avec le rôle: {role}!")
        else:
            ConsoleManager.print_message("Erreur lors de la création du compte. Email ou téléphone déjà utilisé.",
                                         success=False)
