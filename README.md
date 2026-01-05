# 🌟 LIKITA Group - Site Web

Site web institutionnel pour **LIKITA Group**, une organisation dédiée à l'autonomisation des femmes à travers les médias, les événements et l'éducation.

[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat)](LICENSE)

## 🌐 Structure du Projet

### Pages Institutionnelles
- **Accueil** : Page d'accueil avec présentation de l'organisation
- **À propos** : Informations sur LIKITA Group
- **Mot de la Directrice Générale** : Message de Nadine Pulumba
- **Vision, Mission et Valeurs** : Fondements de l'organisation

### Pôles / Services
- **Émission LIKITA** : Émissions et contenus médiatiques
- **LIKITA Events** : Événements et conférences
- **LIKITA Academia** : Formations et webinaires
- **Forum Mwasi Mwinda** : Forum dédié

### Fonctionnalités
- ✅ Inscription en ligne aux événements
- ✅ Inscription aux formations
- ✅ Téléchargement de certificats
- ✅ Espace membre
- ✅ Galerie médias
- ✅ Blog / Articles
- ✅ Commentaires sur les articles
- ✅ Admin Django personnalisé
- ✅ Site responsive (Bootstrap 5)

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip
- virtualenv (recommandé)

### Étapes d'installation

1. **Cloner le projet** (ou naviguer vers le dossier)
```bash
cd "LIKITA Group"
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install django pillow
```

5. **Appliquer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

7. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic
```

8. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

Le site sera accessible à l'adresse : `http://127.0.0.1:8000/`

## 📁 Structure des Applications Django

```
likita_group/
├── apps/
│   ├── core/          # Pages institutionnelles
│   ├── users/         # Utilisateurs et profils
│   ├── media_app/     # Émission LIKITA
│   ├── events/        # LIKITA Events + Forum Mwasi Mwinda
│   ├── academia/      # Formations et certificats
│   └── blog/          # Articles et actualités
├── templates/         # Templates HTML
├── static/           # Fichiers statiques (CSS, JS, images)
└── media/            # Fichiers média uploadés
```

## 🗄️ Modèles Principaux

### Core
- `Membre` : Membres de l'équipe
- `MessageDirectrice` : Message de la Directrice Générale
- `VisionMission` : Vision, mission et valeurs

### Media App
- `Emission` : Émissions LIKITA
- `ArticleEmission` : Articles liés aux émissions

### Events
- `Evenement` : Événements et conférences
- `Inscription` : Inscriptions aux événements
- `GalerieEvenement` : Galerie photo/vidéo

### Academia
- `Formation` : Formations et webinaires
- `InscriptionFormation` : Inscriptions aux formations
- `Certificat` : Certificats délivrés

### Blog
- `Categorie` : Catégories d'articles
- `Article` : Articles de blog
- `Commentaire` : Commentaires sur les articles

### Users
- `ProfilUtilisateur` : Profil étendu des utilisateurs

## 🎨 Technologies Utilisées

- **Backend** : Django 4.2+
- **Frontend** : Bootstrap 5.3, Font Awesome 6.4
- **Base de données** : SQLite (développement)
- **Traitement d'images** : Pillow

## 📝 Configuration

### Fichiers importants
- `likita_group/settings.py` : Configuration Django
- `likita_group/urls.py` : URLs principales
- `templates/base.html` : Template de base

### Variables d'environnement (à configurer en production)
- `SECRET_KEY` : Clé secrète Django
- `DEBUG` : Mode debug (False en production)
- `ALLOWED_HOSTS` : Hôtes autorisés
- `DATABASES` : Configuration de la base de données

## 🔐 Administration

Accéder à l'interface d'administration Django :
```
http://127.0.0.1:8000/admin/
```

Utiliser les identifiants du superutilisateur créé.

## 📱 Fonctionnalités Utilisateur

### Inscription et Connexion
- Création de compte
- Connexion / Déconnexion
- Profil utilisateur

### Événements
- Liste des événements
- Détail d'un événement
- Inscription en ligne
- Suivi des inscriptions

### Formations
- Liste des formations
- Détail d'une formation
- Inscription en ligne
- Téléchargement de certificats

### Émissions
- Liste des émissions
- Visionnage des vidéos
- Articles liés

### Blog
- Liste des articles
- Lecture d'articles
- Commentaires
- Recherche et filtres

## 🛠️ Développement

### Commandes utiles

```bash
# Créer une nouvelle migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer les tests
python manage.py test

# Accéder au shell Django
python manage.py shell
```

## 🚀 Déploiement

### Préparation pour la production

1. **Modifier les settings de production** :
   - Changer `DEBUG = False`
   - Configurer `ALLOWED_HOSTS`
   - Générer une nouvelle `SECRET_KEY`
   - Configurer une vraie base de données (PostgreSQL recommandé)

2. **Collecter les fichiers statiques** :
   ```bash
   python manage.py collectstatic
   ```

3. **Configurer le serveur web** (Nginx + Gunicorn recommandé)

## 📄 Licence

Ce projet est la propriété de LIKITA Group. Tous droits réservés.

## 👥 Contact

Pour toute question ou information :
- Email : contact@likitagroup.com
- Téléphone : +243 XXX XXX XXX
- Linktree : https://linktr.ee/likitagroup

## 🤝 Contribution

Ce projet est privé. Pour toute contribution, contactez l'équipe LIKITA Group.

---

**LIKITA Group** - Empowering women through media, events, and education.

Made with ❤️ by LIKITA Group Team



