# AdminConsole – Console dédiée aux administrateurs

Cette interface permet à l’admin de gérer :
- les étudiants (CRUD + notes),
- les classes (CRUD + matières),
- les statistiques,
- les exportations (CSV, JSON, PDF).

---

## Classe : AdminConsole

### 🧱 `__init__(self, utilisateur)`
- **But** : Instancie la console admin avec :
  - l’utilisateur connecté,
  - accès aux repositories : `Utilisateur`, `Etudiant`, `Classe`.

---

## 📋 `afficher_menu_principal(self)`
- **But** : Menu principal de l’admin.
- **Options** :
  1. Gestion des étudiants
  2. Gestion des classes
  3. Classement des étudiants
  4. Moyennes par classe
  5. Exportation & Rapports
  6. Déconnexion

---

## 🎓 Gestion des étudiants

### 📂 `menu_gestion_etudiants(self)`
- Affiche un sous-menu pour :
  - créer, rechercher, modifier, supprimer,
  - ajouter des notes.

---

### ➕ `creer_etudiant(self)`
- Lance `creer_etudiant_avec_numero()` après avoir saisi un téléphone.

### 🔁 `creer_etudiant_avec_numero(self, tel)`
- **Logique** :
  1. Vérifie si étudiant existe déjà.
  2. Si utilisateur existe et est `etudiant` → convertit.
  3. Sinon : saisie manuelle complète.
  - Permet aussi d’ajouter des notes si une classe est affectée.

---

### 📃 `lister_etudiants(self)`
- Affiche un tableau avec :
  - nom, prénom, téléphone, classe, moyenne.

---

### 🔍 `rechercher_etudiant(self)`
- Recherche un étudiant :
  - par nom, prénom, téléphone ou classe.
  - Si pas trouvé par téléphone : propose de le créer.

---

### 📝 `ajouter_notes(self)`
- Permet à l’admin d’ajouter/modifier des notes pour un étudiant.
- Si pas de classe : peut lui affecter une.
- Demande les notes selon les matières définies dans la classe.

---

### ✏️ `modifier_etudiant(self)`
- Mise à jour des infos personnelles d’un étudiant.

---

### ❌ `supprimer_etudiant(self)`
- Supprime un étudiant après confirmation.

---

## 🏫 Gestion des classes

### 📂 `menu_gestion_classes(self)`
- Menu similaire à celui des étudiants (ajout, édition, suppression...).

> *Les méthodes internes ne sont pas montrées ici mais suivent la même logique CRUD + cache.*

---

## 🏆 `classement_etudiants(self)`
- Affiche le **classement par moyenne** :
  - global ou par classe.
  - possibilité de chercher un étudiant spécifique.

---

## 📊 `moyenne_par_classe(self)`
- Liste chaque classe avec sa **moyenne générale calculée**.

---

## 📤 Exportation & Rapports

### 📦 `menu_exportation(self)`
- Menu d'export : CSV, JSON, PDF.

---

### 🧾 `exporter_etudiants_csv(self)`
- Export en `.csv` des étudiants avec :
  - infos personnelles, moyenne, notes.

---

### 🧮 `exporter_moyennes_json(self)`
- Fichier `.json` contenant :
  - chaque classe + moyenne globale.

---

### 📄 `exporter_etudiants_pdf(self)`
- Génère un fichier PDF formaté A4 :
  - liste des étudiants, leurs infos, leurs notes.

---

### 📄 `exporter_etudiants_json(self)`
- Export JSON complet de chaque étudiant :
  - nom, prénom, contact, classe, moyenne, notes.

---

## Résumé de l’utilisation

- `AdminConsole` est le **panneau de gestion total**.
- Utilise tous les repositories du système.
- Chaque modification de données **efface les caches**.
- Permet de gérer **les données, les exports, et les performances** du système.

