from view.ConsoleManager import ConsoleManager
from Repositories.EtudiantRepository import EtudiantRepository
from Repositories.UtilisateurRepository import UtilisateurRepository
from Repositories.ClasseRepository import ClasseRepository

class EtudiantConsole:
    """Console pour les étudiants"""

    def __init__(self, utilisateur):
        self.utilisateur = utilisateur
        self.user_repo = UtilisateurRepository()
        self.etudiant_repo = EtudiantRepository()
        self.classe_repo = ClasseRepository()
        self.etudiant = self.etudiant_repo.rechercher_par_telephone(utilisateur.telephone)

        if not self.etudiant:
            ConsoleManager.print_message("❌ Vous n'êtes pas encore enregistré comme étudiant.", success=False)
            input("Appuyez sur Entrée pour revenir au menu principal...")
            self.etudiant = None

    def afficher_menu_principal(self):
        """Affiche le menu principal pour l'étudiant"""
        if not self.etudiant:
            return

        while True:
            ConsoleManager.print_header(f"CONSOLE ÉTUDIANT - {self.utilisateur.prenom} {self.utilisateur.nom}")

            options = [
                (1, "Consulter mes notes"),
                (2, "Consulter mon classement"),
                (3, "Modifier mes informations"),
                (4, "Se déconnecter")
            ]

            ConsoleManager.print_menu(options)
            choice = ConsoleManager.get_user_choice(1, 4)

            if choice == 1:
                self.consulter_notes()
            elif choice == 2:
                self.consulter_classement()
            elif choice == 3:
                self.modifier_informations()
            else:
                self.user_repo.deconnecter(self.utilisateur.email)
                break

    def consulter_notes(self):
        """Affiche les notes de l'étudiant"""
        ConsoleManager.print_header("MES NOTES")
        if not self.etudiant.notes:
            ConsoleManager.print_message("Aucune note disponible.")
            return

        for matiere, note in self.etudiant.notes.items():
            print(f"{matiere}: {note}/20")

        print(f"\nMoyenne générale: {self.etudiant.calculer_moyenne():.2f}/20")

    def consulter_classement(self):
        """Affiche le classement de l'étudiant"""
        ConsoleManager.print_header("MON CLASSEMENT")
        if not self.etudiant.classe:
            ConsoleManager.print_message("❌ Vous n'êtes affecté à aucune classe.", success=False)
            return

        classement = self.etudiant_repo.trier_par_moyenne(self.etudiant.classe)
        for i, etu in enumerate(classement, 1):
            if etu.telephone == self.etudiant.telephone:
                print(f"🏅 Vous êtes classé {i}ᵉ dans la classe {self.etudiant.classe} avec une moyenne de {etu.calculer_moyenne():.2f}/20")
                return

        ConsoleManager.print_message("Erreur: étudiant non trouvé dans le classement.")

    def modifier_informations(self):
        """Permet à l'étudiant de modifier ses informations personnelles"""
        ConsoleManager.print_header("MODIFIER MES INFORMATIONS")

        updates = {}

        nom = input(f"Nom [{self.etudiant.nom}]: ").strip()
        prenom = input(f"Prénom [{self.etudiant.prenom}]: ").strip()
        email = input(f"Email [{self.etudiant.email}]: ").strip()
        telephone = input(f"Téléphone [{self.etudiant.telephone}]: ").strip()

        if nom: updates["nom"] = nom
        if prenom: updates["prenom"] = prenom
        if email: updates["email"] = email
        if telephone: updates["telephone"] = telephone

        if not updates:
            ConsoleManager.print_message("Aucune modification effectuée.")
            return

        success = self.etudiant_repo.modifier_etudiant(self.etudiant.telephone, updates)

        if success:
            ConsoleManager.print_message("✅ Informations mises à jour.")
            # Mettre à jour localement
            for k, v in updates.items():
                setattr(self.etudiant, k, v)
        else:
            ConsoleManager.print_message("❌ Échec de la mise à jour.", success=False)
