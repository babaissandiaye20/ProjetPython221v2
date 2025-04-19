# AuthConsole – Console de connexion et création de comptes

Cette classe est **le point d’entrée du système**.
Elle permet :
- la connexion des utilisateurs (admin, enseignant, étudiant),
- la création de compte avec choix de rôle,
- la redirection vers la console liée au rôle.

---

## Classe : AuthConsole

### 🧱 `__init__(self)`
- **But** : Initialise la console.
- **Composants** :
  - `UtilisateurRepository()` : pour gérer les comptes.

---

## 📋 `afficher_menu_principal(self)`
- **But** : Affiche le menu principal à l’ouverture du programme.
- **Options** :
  1. Se connecter
  2. Créer un compte
  3. Quitter
- **Logique** :
  - Choix 1 → appelle `ecran_connexion()`
  - Choix 2 → appelle `ecran_creation_compte()`
  - Choix 3 → quitte proprement

---

## 🔐 `ecran_connexion(self)`
- **But** : Permet à un utilisateur de se connecter.
- **Étapes** :
  1. Demande `email` et `mot_de_passe`.
  2. Utilise `UtilisateurRepository.authentifier()` :
     - Si OK → affiche message de bienvenue.
     - Redirige vers :
       - `AdminConsole` si `role == admin`
       - `EnseignantConsole` si `role == enseignant`
       - `EtudiantConsole` si `role == etudiant`
     - Si KO → message d’erreur.

---

## 🆕 `ecran_creation_compte(self)`
- **But** : Crée un nouveau compte utilisateur.
- **Étapes** :
  1. Demande infos : `nom`, `prénom`, `téléphone`, `email`, `mot_de_passe`.
  2. Affiche un menu pour choisir le rôle :
     - 1 → `etudiant`
     - 2 → `enseignant`
     - 3 → `admin`
  3. Crée un objet `Utilisateur`.
  4. Appelle `UtilisateurRepository.creer_utilisateur()` pour insertion.
  5. Affiche un message de confirmation ou d’échec.

---

## Résumé de l’utilisation

- `AuthConsole` est **le premier contact** de l’utilisateur avec le système.
- Elle fait le **pont entre l’authentification** et les interfaces (admin, prof, étudiant).
- Toute la logique d'accès au système **passe par elle**.
- La validation de rôle est directe, le routage est propre.

