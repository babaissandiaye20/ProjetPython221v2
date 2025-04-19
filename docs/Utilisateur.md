# Utilisateur – Représente un compte utilisateur de la plateforme

Cette classe gère les données de tout utilisateur (admin, enseignant, étudiant).

---

## Classe : Utilisateur

### 👥 Attributs principaux
- `nom`, `prenom`, `telephone`, `email` : informations d’identité.
- `mot_de_passe` : mot de passe (en clair à la création, haché ensuite).
- `role` : un des rôles définis dans `ROLES`.

---

### 🔁 `ROLES = ["admin", "enseignant", "etudiant"]`
- Définition des rôles possibles pour les utilisateurs.
- Si un rôle non reconnu est passé → assigné à "etudiant" par défaut.

---

### 🧱 `__init__(self, nom, prenom, telephone, email, mot_de_passe, role="etudiant")`
- **But** : Crée un nouvel utilisateur.
- **Logique** :
  - Le rôle est vérifié.
  - Si non reconnu → assignation par défaut à `"etudiant"`.

---

### 👁 `afficher_infos(self)`
- **But** : Retourne un résumé textuel sans mot de passe.
- **Format** :
