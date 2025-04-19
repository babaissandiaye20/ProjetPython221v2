from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from Repositories.view.ConsoleManager import ConsoleManager
from Repositories.UtilisateurRepository import UtilisateurRepository
from Repositories.EtudiantRepository import EtudiantRepository
from Repositories.ClasseRepository import ClasseRepository
from Models.Etudiant import Etudiant
import csv
import json
from datetime import datetime
import os

class AdminConsole:
    def __init__(self, utilisateur):
        self.utilisateur = utilisateur
        self.user_repo = UtilisateurRepository()
        self.etudiant_repo = EtudiantRepository()
        self.classe_repo = ClasseRepository()

    def afficher_menu_principal(self):
        while True:
            ConsoleManager.print_header("CONSOLE ADMINISTRATEUR")
            options = [
                (1, "Gestion des étudiants"),
                (2, "Gestion des classes"),
                (3, "Classement des étudiants"),
                (4, "Moyennes par classe"),
                (5, "Exportation & Rapports"),
                (6, "Déconnexion")
            ]
            ConsoleManager.print_menu(options)
            choix = ConsoleManager.get_user_choice(1, 6)

            match choix:
                case 1: self.menu_gestion_etudiants()
                case 2: self.menu_gestion_classes()
                case 3: self.classement_etudiants()
                case 4: self.moyenne_par_classe()
                case 5: self.menu_exportation()
                case 6:
                    ConsoleManager.print_message("Déconnexion réussie.")
                    break

    def menu_gestion_etudiants(self):
        while True:
            ConsoleManager.print_header("GESTION DES ÉTUDIANTS")
            options = [
                (1, "Créer un étudiant"),
                (2, "Lister tous les étudiants"),
                (3, "Rechercher un étudiant"),
                (4, "Ajouter/modifier une note"),
                (5, "Modifier un étudiant"),
                (6, "Supprimer un étudiant"),
                (7, "Retour")
            ]
            ConsoleManager.print_menu(options)
            choix = ConsoleManager.get_user_choice(1, 7)

            match choix:
                case 1: self.creer_etudiant()
                case 2: self.lister_etudiants()
                case 3: self.rechercher_etudiant()
                case 4: self.ajouter_notes()
                case 5: self.modifier_etudiant()
                case 6: self.supprimer_etudiant()
                case 7: break

    def creer_etudiant(self):
        ConsoleManager.print_header("CRÉATION D'UN ÉTUDIANT")
        tel = input("Téléphone: ").strip()
        self.creer_etudiant_avec_numero(tel)

    def creer_etudiant_avec_numero(self, tel):
        if self.etudiant_repo.rechercher_par_telephone(tel):
            ConsoleManager.print_message("❌ Étudiant déjà existant.", success=False)
            return

        utilisateur = self.user_repo.rechercher_par_telephone(tel)

        if utilisateur and utilisateur.role == "etudiant":
            ConsoleManager.print_message(f"✅ Utilisateur trouvé: {utilisateur.prenom} {utilisateur.nom}")
            classe = input("Classe à affecter (optionnel): ").strip()

            if classe and not self.classe_repo.rechercher_par_nom(classe):
                ConsoleManager.print_message("❌ Classe introuvable.", success=False)
                return

            self.etudiant_repo.creer_depuis_utilisateur(utilisateur, classe or None)
            ConsoleManager.print_message("✅ Étudiant créé depuis utilisateur.")
            return

        if utilisateur:
            ConsoleManager.print_message(
                f"❌ Ce numéro est déjà utilisé par un compte '{utilisateur.role}'. Impossible de créer un étudiant.",
                success=False)
            return

        ConsoleManager.print_message("⚠️ Aucun utilisateur existant. Saisie manuelle complète.")
        tel = input("Téléphone (à saisir à nouveau) : ").strip()
        nom = input("Nom: ").strip()
        prenom = input("Prénom: ").strip()
        email = input("Email: ").strip()
        classe = input("Classe (optionnel): ").strip()

        if classe and not self.classe_repo.rechercher_par_nom(classe):
            ConsoleManager.print_message("❌ Classe introuvable.", success=False)
            return

        etudiant = Etudiant(nom, prenom, tel, email, classe or None)

        if classe:
            classe_obj = self.classe_repo.rechercher_par_nom(classe)
            for mat in classe_obj.matieres:
                note = input(f"Note pour {mat} (0-20 ou vide): ").strip()
                if note:
                    try:
                        val = float(note)
                        if 0 <= val <= 20:
                            etudiant.ajouter_note(mat, val)
                    except ValueError:
                        pass

        if self.etudiant_repo.creer_etudiant(etudiant):
            ConsoleManager.print_message("✅ Étudiant ajouté.")
        else:
            ConsoleManager.print_message("❌ Échec ajout.", success=False)

    def lister_etudiants(self):
        ConsoleManager.print_header("LISTE DES ÉTUDIANTS")
        etudiants = self.etudiant_repo.lister_tous()
        if not etudiants:
            ConsoleManager.print_message("Aucun étudiant.")
            return

        print(f"{'Nom':<15}{'Prénom':<15}{'Téléphone':<15}{'Classe':<10}{'Moyenne':<7}")
        print("-" * 65)
        for e in etudiants:
            print(f"{e.nom:<15}{e.prenom:<15}{e.telephone:<15}{e.classe or '---':<10}{e.calculer_moyenne():<7.2f}")

    def rechercher_etudiant(self):
        ConsoleManager.print_header("RECHERCHE ÉTUDIANT")
        options = [
            (1, "Par nom"),
            (2, "Par prénom"),
            (3, "Par téléphone"),
            (4, "Par classe")
        ]
        ConsoleManager.print_menu(options)
        choix = ConsoleManager.get_user_choice(1, 4)

        if choix == 1:
            nom = input("Nom: ").strip()
            resultats = self.etudiant_repo.rechercher_par_nom_prenom(nom)
        elif choix == 2:
            prenom = input("Prénom: ").strip()
            resultats = self.etudiant_repo.rechercher_par_nom_prenom("", prenom)
        elif choix == 3:
            tel = input("Téléphone: ").strip()
            etu = self.etudiant_repo.rechercher_par_telephone(tel)
            if not etu:
                ConsoleManager.print_message("❌ Étudiant introuvable.")
                reponse = input("Souhaitez-vous créer un étudiant avec ce numéro ? (oui/non) : ").strip().lower()
                if reponse == "oui":
                    self.creer_etudiant_avec_numero(tel)
                return
            resultats = [etu]
        else:
            classe = input("Classe: ").strip()
            resultats = self.etudiant_repo.rechercher_par_classe(classe)

        if not resultats:
            ConsoleManager.print_message("Aucun résultat.")
        else:
            for e in resultats:
                print(e.afficher_infos())

    def ajouter_notes(self):
        ConsoleManager.print_header("AJOUT / MODIF DE NOTE")
        tel = input("Téléphone étudiant: ").strip()
        etu = self.etudiant_repo.rechercher_par_telephone(tel)
        if not etu:
            ConsoleManager.print_message("Étudiant introuvable.", success=False)
            return

        if not etu.classe:
            classe = input("Affecter une classe: ").strip()
            if not self.classe_repo.rechercher_par_nom(classe):
                ConsoleManager.print_message("Classe inconnue.", success=False)
                return
            self.etudiant_repo.modifier_etudiant(tel, {"classe": classe})
            etu.classe = classe

        classe_obj = self.classe_repo.rechercher_par_nom(etu.classe)
        if not classe_obj or not classe_obj.matieres:
            ConsoleManager.print_message("Pas de matières définies.")
            return

        for mat in classe_obj.matieres:
            note = input(f"Note pour {mat} (0-20 ou vide): ").strip()
            if note:
                try:
                    val = float(note)
                    if 0 <= val <= 20:
                        self.etudiant_repo.ajouter_note(tel, mat, val)
                except ValueError:
                    continue

        ConsoleManager.print_message("✅ Notes mises à jour.")

    def modifier_etudiant(self):
        ConsoleManager.print_header("MODIFIER UN ÉTUDIANT")
        tel = input("Téléphone actuel: ").strip()
        etu = self.etudiant_repo.rechercher_par_telephone(tel)
        if not etu:
            ConsoleManager.print_message("Étudiant introuvable.", success=False)
            return

        updates = {}
        nom = input(f"Nom [{etu.nom}]: ").strip()
        prenom = input(f"Prénom [{etu.prenom}]: ").strip()
        email = input(f"Email [{etu.email}]: ").strip()
        new_tel = input(f"Téléphone [{etu.telephone}]: ").strip()
        classe = input(f"Classe [{etu.classe or '---'}]: ").strip()

        if nom: updates["nom"] = nom
        if prenom: updates["prenom"] = prenom
        if email: updates["email"] = email
        if new_tel: updates["telephone"] = new_tel
        if classe:
            if not self.classe_repo.rechercher_par_nom(classe):
                ConsoleManager.print_message("Classe inconnue.", success=False)
                return
            updates["classe"] = classe

        if updates:
            if self.etudiant_repo.modifier_etudiant(tel, updates):
                ConsoleManager.print_message("✅ Étudiant modifié.")
            else:
                ConsoleManager.print_message("❌ Échec modification.", success=False)
        else:
            ConsoleManager.print_message("Aucune modification.")

    def supprimer_etudiant(self):
        ConsoleManager.print_header("SUPPRESSION ÉTUDIANT")
        tel = input("Téléphone: ").strip()
        etu = self.etudiant_repo.rechercher_par_telephone(tel)
        if not etu:
            ConsoleManager.print_message("Étudiant introuvable.", success=False)
            return

        confirm = input(f"Confirmer suppression {etu.nom} {etu.prenom} ? (oui/non): ").lower()
        if confirm == "oui":
            if self.etudiant_repo.supprimer_etudiant(tel):
                ConsoleManager.print_message("✅ Étudiant supprimé.")
            else:
                ConsoleManager.print_message("❌ Erreur suppression.", success=False)

    def classement_etudiants(self):
        ConsoleManager.print_header("CLASSEMENT DES ÉTUDIANTS")
        print("1. Tous les étudiants (triés par moyenne)")
        print("2. Par classe")
        print("3. Rechercher un étudiant spécifique")
        choix = ConsoleManager.get_user_choice(1, 3)

        if choix == 1:
            etudiants = self.etudiant_repo.trier_par_moyenne()
            print("\\nClassement global :")
            for i, e in enumerate(etudiants, 1):
                print(f"{i}. {e.nom} {e.prenom} - {e.classe or 'Non assigné'} - Moyenne: {e.calculer_moyenne():.2f}")

        elif choix == 2:
            classe = input("Nom de la classe: ").strip()
            etudiants = self.etudiant_repo.trier_par_moyenne(classe)
            if not etudiants:
                ConsoleManager.print_message("❌ Aucun étudiant trouvé pour cette classe.", success=False)
                return
            print(f"\\nClassement pour la classe {classe} :")
            for i, e in enumerate(etudiants, 1):
                print(f"{i}. {e.nom} {e.prenom} - Moyenne: {e.calculer_moyenne():.2f}")

        elif choix == 3:
            tel = input("Téléphone de l'étudiant: ").strip()
            etudiant = self.etudiant_repo.rechercher_par_telephone(tel)
            if not etudiant:
                ConsoleManager.print_message("❌ Étudiant introuvable.", success=False)
                return
            print("\\nInformations sur l'étudiant :")
            print(etudiant.afficher_infos())

    def moyenne_par_classe(self):
        ConsoleManager.print_header("MOYENNE PAR CLASSE")
        classes = self.classe_repo.lister_toutes()
        for c in classes:
            moy = self.etudiant_repo.calculer_moyenne_classe(c.nom)
            print(f"{c.nom}: {moy}/20")

    def menu_exportation(self):
        ConsoleManager.print_header("EXPORTATION & RAPPORTS")
        options = [
            (1, "Exporter tous les étudiants (CSV)"),
            (2, "Exporter moyennes par classe (JSON)"),
            (3, "Exporter tous les étudiants (PDF)"),
            (4, "Retour")
        ]
        ConsoleManager.print_menu(options)
        choix = ConsoleManager.get_user_choice(1, 4)

        match choix:
            case 1:
                self.exporter_etudiants_csv()
            case 2:
                self.exporter_etudiants_json()
            case 3:
                self.exporter_etudiants_pdf()
            case 4:
                return

    def exporter_etudiants_csv(self):
        etudiants = self.etudiant_repo.lister_tous()
        if not etudiants:
            ConsoleManager.print_message("Aucun étudiant à exporter.", success=False)
            return

        dossier = os.path.join("Data", "exports", "CSV")
        os.makedirs(dossier, exist_ok=True)
        nom_fichier = os.path.join(dossier, f"etudiants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

        lignes = []
        for e in etudiants:
            moyenne = e.calculer_moyenne()
            notes_str = "; ".join([f"{m}: {n}/20" for m, n in e.notes.items()])
            lignes.append([e.nom, e.prenom, e.telephone, e.email, e.classe or "---", moyenne, notes_str])

        with open(nom_fichier, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Nom", "Prénom", "Téléphone", "Email", "Classe", "Moyenne", "Notes"])
            writer.writerows(lignes)

        ConsoleManager.print_message(f"✅ Étudiants exportés dans {nom_fichier}")

    def exporter_moyennes_json(self):
        classes = self.classe_repo.lister_toutes()
        if not classes:
            ConsoleManager.print_message("Aucune classe à traiter.", success=False)
            return

        moyennes = {}
        for c in classes:
            moyennes[c.nom] = self.etudiant_repo.calculer_moyenne_classe(c.nom)

        dossier = os.path.join("Data", "exports", "Json")
        os.makedirs(dossier, exist_ok=True)
        nom_fichier = os.path.join(dossier, f"moyennes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        with open(nom_fichier, mode='w', encoding='utf-8') as file:
            json.dump(moyennes, file, indent=4, ensure_ascii=False)
        ConsoleManager.print_message(f"✅ Moyennes exportées dans {nom_fichier}")

    def exporter_etudiants_pdf(self):
        etudiants = self.etudiant_repo.lister_tous()
        if not etudiants:
            ConsoleManager.print_message("Aucun étudiant à exporter.", success=False)
            return

        dossier = os.path.join("Data", "exports", "PDF")
        os.makedirs(dossier, exist_ok=True)
        nom_fichier = os.path.join(dossier, f"etudiants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

        c = canvas.Canvas(nom_fichier, pagesize=A4)
        largeur, hauteur = A4
        c.setFont("Helvetica", 12)
        y = hauteur - 50

        c.drawString(200, y, "Liste des étudiants")
        y -= 30
        c.setFont("Helvetica", 10)

        for e in etudiants:
            infos = f"{e.nom} {e.prenom} | Tel: {e.telephone} | Classe: {e.classe or '---'} | Moyenne: {e.calculer_moyenne():.2f}"
            notes = ", ".join([f"{mat}: {note}/20" for mat, note in e.notes.items()])
            c.drawString(50, y, infos)
            y -= 15
            c.drawString(60, y, f"Notes: {notes}")
            y -= 25
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = hauteur - 50

        c.save()
        ConsoleManager.print_message(f"✅ Étudiants exportés dans {nom_fichier}")

    def exporter_etudiants_json(self):
        etudiants = self.etudiant_repo.lister_tous()
        if not etudiants:
            ConsoleManager.print_message("Aucun étudiant à exporter.", success=False)
            return

        dossier = os.path.join("Data", "exports", "Json")
        os.makedirs(dossier, exist_ok=True)
        nom_fichier = os.path.join(dossier, f"etudiants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        data = []
        for e in etudiants:
            data.append({
                "nom": e.nom,
                "prenom": e.prenom,
                "telephone": e.telephone,
                "email": e.email,
                "classe": e.classe,
                "moyenne": e.calculer_moyenne(),
                "notes": e.notes
            })

        with open(nom_fichier, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        ConsoleManager.print_message(f"✅ Étudiants exportés en JSON dans {nom_fichier}")


def exporter_etudiants_json(self):
    etudiants = self.etudiant_repo.lister_tous()
    if not etudiants:
        ConsoleManager.print_message("Aucun étudiant à exporter.", success=False)
        return

    dossier = os.path.join("Data", "exports", "Json")
    os.makedirs(dossier, exist_ok=True)
    nom_fichier = os.path.join(dossier, f"etudiants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    data = []
    for e in etudiants:
        data.append({
            "nom": e.nom,
            "prenom": e.prenom,
            "telephone": e.telephone,
            "email": e.email,
            "classe": e.classe,
            "moyenne": e.calculer_moyenne(),
            "notes": e.notes
        })

    with open(nom_fichier, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    ConsoleManager.print_message(f"✅ Étudiants exportés en JSON dans {nom_fichier}")
