# EtudiantRepository – Gère les étudiants dans MongoDB + Redis

Ce repository centralise toutes les opérations concernant les étudiants :
- création,
- recherche,
- modification,
- suppression,
- gestion des notes,
- calculs de moyenne,
- tri,
- export...

---

## Classe : EtudiantRepository

### 🧱 `__init__(self)`
- **But** : Initialise le repository.
- **Composants** :
  - `MongoDB()` : accès base principale.
  - `RedisDB()` : système de cache.
  - `collection_name = "etudiants"` : nom Mongo utilisé.

---

### 🆕 `creer_etudiant(self, etudiant)`
- **But** : Enregistre un nouvel étudiant.
- **Logique** :
  - Vérifie unicité du `telephone`.
  - Vérifie que les notes (si présentes) sont valides (0–20).
  - Insère dans Mongo.
  - Met en cache avec clé `etudiant:<tel>`.

---

### 🧩 `creer_depuis_utilisateur(self, utilisateur, classe=None)`
- **But** : Transforme un `Utilisateur` en `Etudiant`.
- **Condition** : uniquement si `utilisateur.role == "etudiant"`.
- **Utilité** : convertir les comptes créés en vrais étudiants.

---

### 🔍 `rechercher_par_telephone(self, telephone)`
- **But** : Recherche un étudiant via son numéro.
- **Logique** :
  - Cherche d’abord dans Redis.
  - Sinon → Mongo, puis enregistre dans le cache.
- **Retour** :
  - `Etudiant` ou `None`.

---

### 🔍 `rechercher_par_nom_prenom(self, nom, prenom=None)`
- **But** : Recherche des étudiants par nom/prénom.
- **Mongo** : Utilise des regex pour recherche partielle.
- **Cache** : utilise `find_with_cache()` de Redis pour performance.
- **Retour** : liste d’objets `Etudiant`.

---

### 🏫 `rechercher_par_classe(self, classe)`
- **But** : Récupère tous les étudiants d’une classe donnée.
- **Cache** : clé `classe:<nom>:etudiants`.
- **Retour** : liste d’objets `Etudiant`.

---

### 📜 `lister_tous(self)`
- **But** : Liste de tous les étudiants.
- **Cache** : clé `etudiants:all`.
- **Mongo** : si cache manquant.
- **Retour** : liste `Etudiant`.

---

### 📝 `ajouter_note(self, telephone, matiere, note)`
- **But** : Ajoute/modifie une note pour un étudiant.
- **Condition** : note entre 0 et 20.
- **Efface** : tous les caches associés à l’étudiant et sa classe.

---

### ✏️ `modifier_etudiant(self, telephone, nouvelles_donnees)`
- **But** : Met à jour les infos d’un étudiant.
- **Vérifie** : que les notes restent valides si fournies.
- **Efface** : tous les caches impactés (étudiant + classe si modifiée).

---

### ❌ `supprimer_etudiant(self, telephone)`
- **But** : Supprime un étudiant de MongoDB.
- **Efface** : tous les caches liés (profil, classe, liste globale).
- **Retour** : `True` si suppression OK, sinon `False`.

---

### 📊 `trier_par_moyenne(self, classe=None, limit=None)`
- **But** : Retourne les étudiants triés par moyenne (décroissant).
- **Filtrage** : optionnel par classe.
- **Limit** : optionnel → top N.
- **Retour** : liste ordonnée d’objets `Etudiant`.

---

### 🧮 `calculer_moyenne_classe(self, classe)`
- **But** : Moyenne générale des étudiants d’une classe.
- **Retour** :
  - `0.0` si aucun étudiant.
  - Moyenne arrondie sinon.

---

## Résumé de l’utilisation

- `EtudiantRepository` est la **colonne vertébrale** pour tout ce qui touche aux élèves.
- Toutes les consoles (admin, enseignant, étudiant) l’utilisent.
- Les caches sont systématiquement gérés pour éviter les redondances.
- C’est le repository le plus riche fonctionnellement de l’application.

