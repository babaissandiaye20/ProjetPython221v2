# UtilisateurRepository – Gère l’enregistrement, l’authentification et la gestion des comptes utilisateurs

Ce repository permet :
- de créer un compte utilisateur,
- de le connecter via mot de passe (bcrypt),
- de gérer sessions et rôles,
- de modifier mot de passe et rôle,
- de vérifier des tokens d’authentification.

---

## Classe : UtilisateurRepository

### 🧱 `__init__(self)`
- **But** : Initialise le repository.
- **Composants** :
  - `MongoDB()` : accès base principale.
  - `RedisDB()` : système de cache.
  - `collection_name = "utilisateurs"`
  - `session_collection = "sessions"`

---

### 🆕 `creer_utilisateur(self, utilisateur, role=None)`
- **But** : Crée un nouvel utilisateur.
- **Vérifie** :
  - Email et téléphone non utilisés.
- **Hashage** :
  - Mot de passe est haché avec `bcrypt`.
- **Insertion** : dans MongoDB.
- **Retour** :
  - `ObjectId` si succès.
  - `None` sinon.

---

### 🔐 `authentifier(self, email, mot_de_passe)`
- **But** : Authentifie un utilisateur via son email + mot de passe.
- **Étapes** :
  1. Vérifie d’abord dans Redis (`auth:<email>`).
  2. Si absent → recherche Mongo, compare mot de passe haché.
  3. Si OK :
     - Génère un `token` UUID.
     - Crée une session Mongo avec expiration (1h).
     - Cache les données dans Redis (avec token).
- **Retour** :
  - `(Utilisateur, token)` si succès.
  - `(None, None)` si échec.

---

### 🚪 `deconnecter(self, email)`
- **But** : Supprime la session d’un utilisateur (Mongo + Redis).

---

### 🧾 `verifier_token(self, token)`
- **But** : Vérifie la validité d’un token de session.
- **Logique** :
  - Cherche en Mongo.
  - Si token expiré → supprime la session.
- **Retour** :
  - Dictionnaire session si valide.
  - `None` sinon.

---

### 🔑 `modifier_mot_de_passe(self, email, ancien, nouveau)`
- **But** : Change le mot de passe après vérification de l’ancien.
- **Logique** :
  - Compare mot de passe avec `bcrypt.checkpw`.
  - Hash le nouveau.
  - Met à jour en Mongo.
  - Déconnecte l’utilisateur (force reconnexion).
- **Retour** :
  - `True` si OK.
  - `False` sinon.

---

### 🎭 `modifier_role(self, email, nouveau_role)`
- **But** : Change le rôle d’un utilisateur.
- **Validation** : rôle doit faire partie de `Utilisateur.ROLES`.
- **Efface** : le cache auth Redis (`auth:<email>`).

---

### 🔍 `rechercher_par_telephone(self, telephone)`
- **But** : Recherche un utilisateur via son téléphone.
- **Retour** : objet `Utilisateur` ou `None`.

---

## Résumé de l’utilisation

- `UtilisateurRepository` est le cœur de la **gestion des comptes**.
- Il gère :
  - la sécurité via `bcrypt`,
  - les sessions temporaires via MongoDB et Redis,
  - les rôles et permissions.
- Utilisé principalement dans :
  - `AuthConsole`
  - `AdminConsole`
  - `EtudiantConsole`
  - `EnseignantConsole`

