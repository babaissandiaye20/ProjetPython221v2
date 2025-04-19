# RedisDB – Singleton pour la gestion du cache avec Redis

Ce fichier contient une classe `RedisDB` et un encodeur JSON personnalisé pour intégrer Redis comme système de cache.

## Classe : JSONEncoder

### 🔁 `default(self, obj)`
- **But** : Convertit les objets non sérialisables par défaut (ex: `ObjectId`) en chaînes.
- **Spécificité** : si `obj` est un `ObjectId` MongoDB, il est transformé avec `str(obj)`.

## Classe : RedisDB

### 🧠 Singleton via `__new__(cls)`
- **But** : Empêche la création de plusieurs instances de la connexion Redis.
- **Connexion** : Utilise les paramètres du fichier `config.py` : `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`.

### ✅ `ping(self)`
- **But** : Vérifie la connexion à Redis.
- **Retour** : `True` si Redis répond, sinon exception levée.

### 💾 `set_cache(self, key, value, expire=None)`
- **But** : Enregistre une valeur en cache avec une clé.
- **Paramètres** :
  - `key` : clé unique de cache.
  - `value` : les données à stocker (objet Python).
  - `expire` : durée de vie du cache en secondes (facultatif).
- **Traitement** : Sérialise les objets (ex: `ObjectId`) via le `JSONEncoder` personnalisé.

### 📥 `get_cache(self, key)`
- **But** : Récupère une donnée du cache.
- **Retour** :
  - Si la clé existe : valeur désérialisée en Python.
  - Sinon : `None`.

### ❌ `delete(self, key)`
- **But** : Supprime une clé du cache Redis.

### 🔄 `find_with_cache(self, collection_name, query, mongo_instance, expire=60)`
- **But** : Requête MongoDB **avec cache intégré**.
- **Logique** :
  1. Génère une clé unique (hashée) à partir de la requête.
  2. Si la donnée est dans Redis : retour immédiat ✅.
  3. Sinon : interroge MongoDB, stocke en cache, et renvoie les résultats 🔁.

- **Paramètres** :
  - `collection_name` : nom de la collection Mongo.
  - `query` : requête Mongo (filtre).
  - `mongo_instance` : instance MongoDB (singleton).
  - `expire` : TTL en secondes (par défaut : 60s).
- **Utilité** : Réduit les accès à MongoDB pour des requêtes identiques.

## Résumé de l’utilisation

- `RedisDB` sert à **mettre en cache les résultats** souvent consultés (étudiants, classes, authentification...).
- `find_with_cache` est utilisé dans les repositories pour éviter des appels inutiles à MongoDB.
- Cela **améliore grandement les performances** de l’application.
