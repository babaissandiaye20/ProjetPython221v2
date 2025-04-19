# ClasseRepository – Interface entre les objets Classe et la base de données

Cette classe gère toutes les opérations liées aux classes :
- création,
- recherche,
- modification,
- suppression,
- gestion des matières,
tout cela via MongoDB + cache Redis.

---

## Classe : ClasseRepository

### 🧱 `__init__(self)`
- **But** : Initialise le repository.
- **Composants** :
  - `MongoDB()` : accès base principale.
  - `RedisDB()` : cache.
  - `collection_name = "classes"` : nom de la collection Mongo utilisée.

---

### 🆕 `creer_classe(self, classe)`
- **But** : Crée une nouvelle classe si elle n’existe pas déjà.
- **Logique** :
  - Vérifie si le nom est déjà pris dans Mongo.
  - Si non → insère via `MongoDB.insert`.
  - Invalide les caches associés (`classes:all`).
- **Retour** :
  - `ObjectId` si succès.
  - `None` si échec.

---

### 🔍 `rechercher_par_nom(self, nom)`
- **But** : Recherche une classe par son nom.
- **Étapes** :
  1. Vérifie dans Redis avec clé `classe:<nom>`.
  2. Si cache vide → requête Mongo.
  3. Met à jour le cache avec expiration.
- **Retour** :
  - Instance de `Classe`, ou `None`.

---

### 📜 `lister_toutes(self)`
- **But** : Récupère toutes les classes.
- **Logique** :
  - Cache Redis `classes:all`.
  - Si absent, va chercher en Mongo.
  - Mets à jour le cache.
- **Retour** :
  - Liste d’objets `Classe`.

---

### ➕ `ajouter_matiere(self, nom_classe, matiere)`
- **But** : Ajoute une matière dans une classe existante.
- **Requête Mongo** : `{"$push": {"matieres": matiere}}`.
- **Nettoyage cache** :
  - Supprime `classe:<nom>` et `classes:all`.

---

### ➖ `supprimer_matiere(self, nom_classe, matiere)`
- **But** : Retire une matière de la classe.
- **Requête Mongo** : `{"$pull": {"matieres": matiere}}`.
- **Mêmes effets sur le cache** que `ajouter_matiere`.

---

### ✏️ `modifier_classe(self, nom, nouvelles_donnees)`
- **But** : Met à jour les attributs d'une classe (nom, année, niveau, etc.).
- **Requête Mongo** : `{"$set": nouvelles_donnees}`.
- **Efface le cache** pour assurer cohérence.

---

### ❌ `supprimer_classe(self, nom)`
- **But** : Supprime une classe par son nom.
- **Actions** :
  - Supprime de Mongo.
  - Nettoie plusieurs clés Redis :
    - `classe:<nom>`
    - `classes:all`
    - `classe:<nom>:etudiants`

---

## Résumé de l’utilisation

- `ClasseRepository` est l’interface entre les objets `Classe` et les bases de données.
- Chaque méthode s’assure de **nettoyer les caches** après une modification.
- Le code exploite **le cache Redis** pour éviter les requêtes répétées en lecture.
- Ce repository est utilisé dans :
  - `AdminConsole`
  - `EtudiantRepository`
  - `EnseignantConsole`

