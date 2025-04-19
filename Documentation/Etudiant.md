# Etudiant – Représente un élève avec ses informations et notes

Cette classe représente un étudiant avec :
- des **infos personnelles**
- sa **classe d’affectation**
- ses **notes par matière**

---

## Classe : Etudiant

### 🧱 `__init__(self, nom, prenom, telephone, email, classe=None, notes=None)`
- **But** : Initialise un nouvel étudiant.
- **Attributs** :
  - `nom`, `prenom`, `telephone`, `email` : données personnelles.
  - `classe` : classe associée (string ou None).
  - `notes` : dictionnaire `{matière: note}`.
- **Remarque** : `notes` est vide par défaut si non fourni.

---

### 🧮 `calculer_moyenne(self)`
- **But** : Calcule la moyenne générale de l’élève.
- **Retour** :
  - Moyenne arrondie à deux décimales.
  - `0` si aucune note.

---

### ➕ `ajouter_note(self, matiere, note)`
- **But** : Ajoute ou met à jour une note pour une matière.
- **Contrôle** :
  - Note doit être entre 0 et 20.
- **Retour** :
  - `True` si la note est valide et ajoutée.
  - `False` sinon.

---

### ➖ `supprimer_note(self, matiere)`
- **But** : Supprime la note d’une matière spécifique.
- **Retour** :
  - `True` si la matière existait.
  - `False` sinon.

---

### 👁 `afficher_infos(self)`
- **But** : Retourne une chaîne contenant toutes les infos de l’étudiant (y compris notes et moyenne).
- **Format** :
