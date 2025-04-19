# EnseignantConsole – Interface dédiée aux enseignants

Cette console permet à un enseignant :
- de gérer les notes des étudiants,
- de voir la liste des élèves,
- de consulter les statistiques par classe.

---

## Classe : EnseignantConsole

### 🧱 `__init__(self, utilisateur)`
- **But** : Initialise la console enseignant avec :
  - l’utilisateur connecté,
  - les repositories `Utilisateur`, `Etudiant`, `Classe`.
- **Auto-chargement** : Aucun étudiant n’est directement lié à l’enseignant ici (pas de restriction).

---

## 📋 `afficher_menu_principal(self)`
- **But** : Affiche les options de gestion disponibles pour le professeur.
- **Options** :
  1. Ajouter / Modifier des notes
  2. Liste des étudiants
  3. Statistiques par classe
  4. Se déconnecter

---

## 📝 `menu_gestion_notes(self)`
- **But** : Permet à l’enseignant d’entrer/modifier des notes.
- **Étapes** :
  1. Saisir téléphone étudiant.
  2. Vérifie si l'étudiant existe + a une classe.
  3. Récupère les matières de la classe.
  4. Demande les notes une par une.
- **Validation** :
  - Chaque note doit être entre 0 et 20.
  - Notes invalides sont ignorées.

---

## 🔔 Alertes intégrées

### 🔻 Cas d’alerte :
1. **Note < 10**
2. **Moyenne par matière < 10**
3. **Moyenne générale < 10**

### 📧 `envoyer_alerte(self, etudiant, matiere, valeur, raison)`
- **But** : Envoie un mail d’alerte à l’étudiant concerné.
- **Logique** :
  - Différents messages selon le type d’alerte.
  - Utilise la fonction `envoyer_email()` pour la notification.

---

## 📃 `afficher_liste_etudiants(self)`
- **But** : Affiche tous les étudiants avec :
  - Nom, prénom, téléphone, classe, moyenne.
- **Source** : via `EtudiantRepository.lister_tous()`.

---

## 📊 `afficher_statistiques(self)`
- **But** : Moyenne générale de chaque classe.
- **Source** : `ClasseRepository.lister_toutes()` + `EtudiantRepository.calculer_moyenne_classe()`.

---

## Résumé de l’utilisation

- `EnseignantConsole` permet un accès ciblé :
  - uniquement sur les **notes** et **performances**.
- Elle **n’a aucun droit de modifier les profils** ou supprimer des données.
- Elle agit **en collaboration avec les repositories**, mais avec des contrôles stricts.
- Le système d’alerte permet une vraie **communication pédagogique proactive**.

