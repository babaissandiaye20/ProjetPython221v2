# Classe – Représente une classe d’élèves (ex: Terminale S)

Cette classe modélise une **classe scolaire** (Terminale A, 5e, etc.) avec ses **matières** et **infos associées**.

---

## Classe : Classe

### 🧱 `__init__(self, nom, niveau, annee_scolaire, matieres=None)`
- **But** : Initialise une instance de classe scolaire.
- **Attributs** :
  - `nom` : nom de la classe (ex: "3e A").
  - `niveau` : niveau (ex: "Collège", "Lycée").
  - `annee_scolaire` : année (ex: "2024-2025").
  - `matieres` : liste des matières enseignées (optionnelle).
- **Logique** : Si `matieres` est `None`, initialise avec une liste vide.

---

### ➕ `ajouter_matiere(self, matiere)`
- **But** : Ajoute une matière à la classe si elle n’est pas déjà présente.
- **Paramètre** : `matiere` (ex: "Maths").
- **Contrôle** : Évite les doublons.

---

### ➖ `supprimer_matiere(self, matiere)`
- **But** : Supprime une matière si elle existe dans la liste.
- **Retour** :
  - `True` si supprimée.
  - `False` si elle n'était pas présente.

---

### 🔄 `to_dict(self)`
- **But** : Convertit l’objet `Classe` en dictionnaire utilisable pour MongoDB.
- **Retour** : dictionnaire avec `nom`, `niveau`, `annee_scolaire`, `matieres`.

---

### 🧬 `@staticmethod from_dict(data)`
- **But** : Recrée un objet `Classe` à partir d’un dictionnaire venant de MongoDB.
- **Paramètre** : `data` (dict avec les attributs de la classe).
- **Retour** : instance de `Classe`.

---

## Résumé de l’utilisation

La classe `Classe` sert à :
- Créer une **entité logique de classe** (Terminale, Seconde...).
- Ajouter ou retirer des **matières**.
- Préparer les données pour Mongo (via `to_dict()`).
- Être rechargée depuis Mongo (via `from_dict()`).

Elle est manipulée principalement dans `ClasseRepository` pour la persistance et la gestion.

