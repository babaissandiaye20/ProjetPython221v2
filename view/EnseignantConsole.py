from view.ConsoleManager import ConsoleManager
from Repositories.UtilisateurRepository import UtilisateurRepository
from Repositories.EtudiantRepository import EtudiantRepository
from Repositories.ClasseRepository import ClasseRepository
from uti.email_sender import envoyer_email


class EnseignantConsole:
    """Console pour les enseignants"""

    def __init__(self, utilisateur):
        self.utilisateur = utilisateur
        self.user_repo = UtilisateurRepository()
        self.etudiant_repo = EtudiantRepository()
        self.classe_repo = ClasseRepository()

    def afficher_menu_principal(self):
        """Affiche le menu principal pour l'enseignant"""
        while True:
            ConsoleManager.print_header(f"CONSOLE ENSEIGNANT - {self.utilisateur.prenom} {self.utilisateur.nom}")

            options = [
                (1, "Ajouter / Modifier des notes"),
                (2, "Liste des étudiants"),
                (3, "Statistiques par classe"),
                (4, "Se déconnecter")
            ]

            ConsoleManager.print_menu(options)
            choice = ConsoleManager.get_user_choice(1, 4)

            match choice:
                case 1: self.menu_gestion_notes()
                case 2: self.afficher_liste_etudiants()
                case 3: self.afficher_statistiques()
                case 4:
                    self.user_repo.deconnecter(self.utilisateur.email)
                    break

    def menu_gestion_notes(self):
        """Ajout ou modification des notes pour un étudiant"""
        ConsoleManager.print_header("AJOUT / MODIFICATION DES NOTES")

        tel = input("Téléphone de l'étudiant : ").strip()
        etu = self.etudiant_repo.rechercher_par_telephone(tel)

        if not etu:
            ConsoleManager.print_message("Étudiant introuvable.", success=False)
            return

        if not etu.classe:
            ConsoleManager.print_message("Étudiant sans classe assignée.", success=False)
            return

        classe = self.classe_repo.rechercher_par_nom(etu.classe)
        if not classe or not classe.matieres:
            ConsoleManager.print_message("Aucune matière trouvée pour cette classe.", success=False)
            return

        for mat in classe.matieres:
            note = input(f"Note pour {mat} (0-20 ou vide pour ignorer): ").strip()
            if note:
                try:
                    val = float(note)
                    if 0 <= val <= 20:
                        self.etudiant_repo.ajouter_note(tel, mat, val)

                        # Alerte 1 : note < 10
                        if val < 10:
                            self.envoyer_alerte(etu, mat, val, raison="note")

                        # Alerte 2 : moyenne matière < 10
                        if mat in etu.notes and etu.notes[mat] < 10:
                            self.envoyer_alerte(etu, mat, etu.notes[mat], raison="matiere")

                    else:
                        ConsoleManager.print_message("Note invalide. Elle doit être entre 0 et 20.", success=False)
                except ValueError:
                    ConsoleManager.print_message("Entrée invalide. Note ignorée.", success=False)

        # Alerte 3 : moyenne générale < 10
        moyenne_gen = etu.calculer_moyenne()
        if moyenne_gen < 10:
            self.envoyer_alerte(etu, "Générale", moyenne_gen, raison="generale")

        ConsoleManager.print_message("✅ Notes mises à jour avec succès.")

    def envoyer_alerte(self, etudiant, matiere, valeur, raison):
        """Envoie un email réel si une alerte est nécessaire"""
        if raison == "note":
            sujet = f"Alerte : note insuffisante en {matiere}"
            msg = f"Bonjour {etudiant.prenom},\n\nVous avez eu {valeur}/20 en {matiere}. Il faut redoubler d'efforts."
        elif raison == "matiere":
            sujet = f"Alerte : moyenne faible en {matiere}"
            msg = f"Bonjour {etudiant.prenom},\n\nVotre moyenne en {matiere} est de {valeur}/20. Travaillez davantage !"
        elif raison == "generale":
            sujet = "Alerte : moyenne générale faible"
            msg = f"Bonjour {etudiant.prenom},\n\nVotre moyenne générale est tombée à {valeur}/20. Attention !"
        else:
            sujet = "Alerte académique"
            msg = "Bonjour, performance académique insuffisante détectée."

        envoyer_email(etudiant.email, sujet, msg)

    def afficher_liste_etudiants(self):
        """Affiche tous les étudiants"""
        ConsoleManager.print_header("LISTE DES ÉTUDIANTS")

        etudiants = self.etudiant_repo.lister_tous()
        if not etudiants:
            ConsoleManager.print_message("Aucun étudiant trouvé.", success=False)
            return

        print(f"{'Nom':<15}{'Prénom':<15}{'Téléphone':<15}{'Classe':<10}{'Moyenne':<7}")
        print("-" * 65)
        for e in etudiants:
            print(f"{e.nom:<15}{e.prenom:<15}{e.telephone:<15}{e.classe or '---':<10}{e.calculer_moyenne():<7.2f}")

    def afficher_statistiques(self):
        """Affiche la moyenne par classe"""
        ConsoleManager.print_header("STATISTIQUES PAR CLASSE")
        classes = self.classe_repo.lister_toutes()
        if not classes:
            ConsoleManager.print_message("Aucune classe trouvée.", success=False)
            return

        for c in classes:
            moy = self.etudiant_repo.calculer_moyenne_classe(c.nom)
            print(f"{c.nom} : {moy:.2f}/20")
