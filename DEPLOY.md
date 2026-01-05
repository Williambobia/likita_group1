# 🚀 Guide de Déploiement - LIKITA Group

## 📋 Prérequis pour le Déploiement

- Python 3.8+
- Serveur web (Nginx recommandé)
- Serveur d'application (Gunicorn recommandé)
- Base de données (PostgreSQL recommandé pour la production)
- Domaine configuré avec SSL

## 🔧 Configuration Production

### 1. Modifier `settings.py`

Créez un fichier `settings_production.py` ou modifiez `settings.py` :

```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com', 'www.votre-domaine.com']

# Base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'likita_db',
        'USER': 'likita_user',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Sécurité
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Email (SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe-app'
```

### 2. Générer une nouvelle SECRET_KEY

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 3. Installer les dépendances de production

```bash
pip install django gunicorn psycopg2-binary pillow
```

### 4. Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Créer le superutilisateur

```bash
python manage.py createsuperuser
```

## 🌐 Configuration Nginx

Exemple de configuration Nginx :

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name votre-domaine.com www.votre-domaine.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /static/ {
        alias /path/to/likita_group/staticfiles/;
    }

    location /media/ {
        alias /path/to/likita_group/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔄 Démarrage avec Gunicorn

```bash
gunicorn likita_group.wsgi:application --bind 127.0.0.1:8000 --workers 3
```

## 📝 Checklist de Déploiement

- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` configuré
- [ ] `SECRET_KEY` changé
- [ ] Base de données PostgreSQL configurée
- [ ] Fichiers statiques collectés
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] SSL/HTTPS configuré
- [ ] Email SMTP configuré
- [ ] Backups automatiques configurés
- [ ] Monitoring configuré

---

Pour plus d'informations, consultez la [documentation Django](https://docs.djangoproject.com/en/stable/howto/deployment/).

