# EtudiantConsole – Interface dédiée à l'étudiant connecté

Cette console permet à l'étudiant :
- de consulter ses notes,
- de voir son classement,
- de modifier ses informations personnelles.

---

## Classe : EtudiantConsole

### 🧱 `__init__(self, utilisateur)`
- **But** : Initialise la console étudiante.
- **Logique** :
  - Charge automatiquement l’objet `Etudiant` via son téléphone.
  - Si aucun étudiant n’est trouvé : message d’erreur et retour au menu principal.

---

## 📋 `afficher_menu_principal(self)`
- **But** : Affiche le menu dédié à l’élève connecté.
- **Options** :
  1. Consulter mes notes
  2. Consulter mon classement
  3. Modifier mes informations
  4. Se déconnecter

---

## 🧾 `consulter_notes(self)`
- **But** : Affiche les notes personnelles de l’étudiant.
- **Format** :
  - Liste des matières avec notes.
  - Moyenne générale.

- **Condition** :
  - Si aucune note : message informatif.

---

## 🏅 `consulter_classement(self)`
- **But** : Affiche le classement de l'étudiant dans sa propre classe.
- **Étapes** :
  1. Vérifie que l’étudiant a une classe.
  2. Récupère tous les étudiants de cette classe.
  3. Trie par moyenne.
  4. Affiche le **rang** de l’étudiant.

- **Message spécial** :
  - Affiche une médaille avec le rang (🏅).

---

## ✏️ `modifier_informations(self)`
- **But** : Permet à l’étudiant de modifier ses informations :
  - nom, prénom, email, téléphone.
- **Logique** :
  - Laisse chaque champ vide pour ne pas le modifier.
  - Applique les modifications uniquement si des valeurs ont été saisies.
  - Met à jour l’objet local après modification.

- **Retour utilisateur** :
  - Message de confirmation ou d’échec.

---

## Résumé de l’utilisation

- `EtudiantConsole` est **centrée sur l’expérience individuelle**.
- Elle donne accès uniquement aux **infos personnelles** et à la **performance scolaire**.
- L’étudiant ne peut modifier que **ses propres données**, pas celles des autres.
- C’est une interface **simple, sécurisée et utile**.

