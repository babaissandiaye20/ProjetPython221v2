# MongoDB – Singleton pour la base de données Mongo

Ce fichier contient une classe `MongoDB` permettant d’interagir avec une base MongoDB en utilisant le patron de conception Singleton.

## Classe : MongoDB

### 🔁 `__new__(cls)`
- **But** : Implémente le **pattern Singleton** : une seule instance de la classe sera créée.
- **Logique** :
  - Si aucune instance n’existe (`_instance is None`), on en crée une.
  - Elle se connecte à MongoDB via l’URI défini dans `config.py`.
  - La base est sélectionnée avec `MONGO_DB_NAME`.

### ✅ `insert(self, collection_name, data)`
- **But** : Insère un document dans une collection.
- **Paramètres** :
  - `collection_name` : nom de la collection Mongo.
  - `data` : dictionnaire à insérer.
- **Retour** : l’`ObjectId` du document inséré.

### 🔍 `find(self, collection_name, query)`
- **But** : Récupère les documents correspondant à une requête.
- **Paramètres** :
  - `collection_name` : nom de la collection.
  - `query` : dictionnaire MongoDB pour filtrer.
- **Retour** : liste de résultats (`list`).

### 🔄 `update(self, collection_name, query, update_query)`
- **But** : Met à jour un ou plusieurs documents.
- **Paramètres** :
  - `query` : critère de sélection.
  - `update_query` : données à modifier, typiquement avec `$set`, `$push`, etc.
- **Retour** : objet résultat d’`update_many`.

### ❌ `delete(self, collection_name, query)`
- **But** : Supprime un ou plusieurs documents.
- **Paramètres** :
  - `query` : condition de suppression.
- **Retour** : résultat de `delete_many`.

## Résumé de l’utilisation

Cette classe centralise toutes les interactions avec MongoDB :
- Elle est **instanciée une seule fois** (singleton).
- Elle est **utilisée par tous les repositories** (étudiant, classe, utilisateur).
- Elle isole la logique Mongo : les autres modules n’ont pas besoin de savoir comment fonctionne `pymongo`.

