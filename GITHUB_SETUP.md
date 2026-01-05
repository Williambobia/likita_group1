# 📦 Guide de Configuration GitHub

## ✅ Étape 1 : Dépôt Git Initialisé

Le dépôt Git a été initialisé avec succès dans votre projet local.

## 🚀 Étape 2 : Créer le Dépôt sur GitHub

### Option A : Via l'interface GitHub (Recommandé)

1. **Allez sur GitHub** : https://github.com/new
2. **Créez un nouveau dépôt** :
   - Nom du dépôt : `likita-group-website` (ou un autre nom de votre choix)
   - Description : "Site web institutionnel pour LIKITA Group"
   - Visibilité : **Privé** (recommandé) ou Public
   - **NE COCHEZ PAS** "Initialize this repository with a README"
   - Cliquez sur **"Create repository"**

3. **Copiez l'URL du dépôt** (ex: `https://github.com/votre-username/likita-group-website.git`)

### Option B : Via GitHub CLI (si installé)

```bash
gh repo create likita-group-website --private --description "Site web institutionnel pour LIKITA Group"
```

## 🔗 Étape 3 : Connecter le Dépôt Local à GitHub

Une fois le dépôt créé sur GitHub, exécutez ces commandes :

```bash
# Ajouter le dépôt distant (remplacez par votre URL)
git remote add origin https://github.com/VOTRE-USERNAME/likita-group-website.git

# Vérifier que le remote est bien configuré
git remote -v

# Pousser le code vers GitHub
git branch -M main
git push -u origin main
```

## 🔐 Étape 4 : Authentification GitHub

Si vous êtes invité à vous authentifier :

### Option A : Token d'accès personnel (Recommandé)

1. Allez sur : https://github.com/settings/tokens
2. Cliquez sur **"Generate new token (classic)"**
3. Donnez un nom au token (ex: "LIKITA Group Project")
4. Sélectionnez les permissions : `repo` (toutes)
5. Cliquez sur **"Generate token"**
6. **Copiez le token** (vous ne pourrez plus le voir après)
7. Utilisez le token comme mot de passe lors du `git push`

### Option B : GitHub CLI

```bash
gh auth login
```

## 📝 Étape 5 : Vérification

Après le push, vérifiez que tout est bien sur GitHub :
- Allez sur votre dépôt GitHub
- Vérifiez que tous les fichiers sont présents
- Vérifiez que le README.md s'affiche correctement

## 🔄 Commandes Git Utiles

### Ajouter des modifications

```bash
# Voir les fichiers modifiés
git status

# Ajouter tous les fichiers modifiés
git add .

# Ou ajouter des fichiers spécifiques
git add nom_du_fichier.py

# Faire un commit
git commit -m "Description des modifications"

# Pousser vers GitHub
git push
```

### Créer une nouvelle branche

```bash
# Créer et basculer sur une nouvelle branche
git checkout -b nom-de-la-branche

# Pousser la branche vers GitHub
git push -u origin nom-de-la-branche
```

### Voir l'historique

```bash
git log --oneline
```

## ⚠️ Fichiers Ignorés

Les fichiers suivants sont automatiquement ignorés par Git (définis dans `.gitignore`) :
- `db.sqlite3` (base de données)
- `__pycache__/` (fichiers Python compilés)
- `venv/` (environnement virtuel)
- `/media` (fichiers uploadés)
- `/staticfiles` (fichiers statiques collectés)
- `.env` (variables d'environnement)

## 🔒 Sécurité

⚠️ **IMPORTANT** : Ne commitez JAMAIS :
- La base de données (`db.sqlite3`)
- Les fichiers sensibles (`.env`, `SECRET_KEY`)
- Les fichiers média uploadés par les utilisateurs
- Les mots de passe ou clés API

## 📚 Ressources

- [Documentation Git](https://git-scm.com/doc)
- [Documentation GitHub](https://docs.github.com/)
- [Guide Git pour débutants](https://guides.github.com/)

---

**Note** : Si vous rencontrez des problèmes, vérifiez que :
1. Git est bien installé : `git --version`
2. Vous êtes authentifié sur GitHub
3. L'URL du dépôt distant est correcte : `git remote -v`

