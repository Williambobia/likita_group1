"""
Script pour remplir automatiquement toutes les informations de LIKITA Group
Exécutez ce script pour initialiser la base de données avec les informations complètes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'likita_group.settings')
django.setup()

from apps.core.models import VisionMission, MessageDirectrice

print("=" * 60)
print("Remplissage des informations de LIKITA Group")
print("=" * 60)

# 1. VISION
vision, created = VisionMission.objects.get_or_create(
    type='vision',
    defaults={
        'titre': 'Notre Vision',
        'description': """Devenir un acteur incontournable dans le domaine de la communication et de l'événementiel, en inspirant, connectant et transformant la société. Nous aspirons à créer un environnement où chacun peut s'exprimer librement et contribuer à un dialogue constructif.""",
        'icone': 'fas fa-eye',
        'ordre_affichage': 1,
        'actif': True,
    }
)
if not created:
    vision.description = """Devenir un acteur incontournable dans le domaine de la communication et de l'événementiel, en inspirant, connectant et transformant la société. Nous aspirons à créer un environnement où chacun peut s'exprimer librement et contribuer à un dialogue constructif."""
    vision.save()
print("OK - Vision mise a jour")

# 2. MISSION
mission, created = VisionMission.objects.get_or_create(
    type='mission',
    defaults={
        'titre': 'Notre Mission',
        'description': """Créer des connexions significatives et encourager le partage d'idées à travers des initiatives créatives et innovantes. Nous croyons que la communication est un outil puissant pour bâtir des ponts, favoriser l'inclusion et stimuler le changement positif.""",
        'icone': 'fas fa-bullseye',
        'ordre_affichage': 1,
        'actif': True,
    }
)
if not created:
    mission.description = """Créer des connexions significatives et encourager le partage d'idées à travers des initiatives créatives et innovantes. Nous croyons que la communication est un outil puissant pour bâtir des ponts, favoriser l'inclusion et stimuler le changement positif."""
    mission.save()
print("OK - Mission mise a jour")

# 3. VALEURS
valeurs_data = [
    {
        'titre': 'Inclusivité',
        'description': "Nous donnons la parole à toutes les voix et encourageons la diversité d'opinions.",
        'icone': 'fas fa-users',
        'ordre': 1,
    },
    {
        'titre': 'Créativité',
        'description': "Nous valorisons l'innovation et l'originalité dans chacun de nos projets.",
        'icone': 'fas fa-lightbulb',
        'ordre': 2,
    },
    {
        'titre': 'Engagement',
        'description': "Nous soutenons activement les initiatives ayant un impact positif sur la communauté.",
        'icone': 'fas fa-handshake',
        'ordre': 3,
    },
    {
        'titre': 'Collaboration',
        'description': "Nous croyons en la force du travail d'équipe et des partenariats stratégiques.",
        'icone': 'fas fa-network-wired',
        'ordre': 4,
    },
]

for valeur_data in valeurs_data:
    valeur, created = VisionMission.objects.get_or_create(
        type='valeur',
        titre=valeur_data['titre'],
        defaults={
            'description': valeur_data['description'],
            'icone': valeur_data['icone'],
            'ordre_affichage': valeur_data['ordre'],
            'actif': True,
        }
    )
    if not created:
        valeur.description = valeur_data['description']
        valeur.icone = valeur_data['icone']
        valeur.ordre_affichage = valeur_data['ordre']
        valeur.actif = True
        valeur.save()
    print(f"OK - Valeur '{valeur_data['titre']}' mise a jour")

# 4. OBJECTIFS (créer comme valeurs supplémentaires ou dans une nouvelle section)
objectifs_data = [
    {
        'titre': 'Renforcer la communication',
        'description': "Créer des plateformes et des initiatives qui facilitent le partage d'informations et d'idées.",
        'icone': 'fas fa-comments',
        'ordre': 5,
    },
    {
        'titre': "Promouvoir l'inclusion",
        'description': "Offrir des espaces où toutes les voix sont entendues et respectées.",
        'icone': 'fas fa-heart',
        'ordre': 6,
    },
    {
        'titre': 'Encourager le développement personnel',
        'description': "Proposer des formations pour améliorer les compétences en communication et en leadership.",
        'icone': 'fas fa-user-graduate',
        'ordre': 7,
    },
    {
        'titre': "Organiser des événements à fort impact",
        'description': "Concevoir des rencontres enrichissantes favorisant l'échange et le réseautage.",
        'icone': 'fas fa-calendar-check',
        'ordre': 8,
    },
]

for objectif_data in objectifs_data:
    objectif, created = VisionMission.objects.get_or_create(
        type='valeur',
        titre=objectif_data['titre'],
        defaults={
            'description': objectif_data['description'],
            'icone': objectif_data['icone'],
            'ordre_affichage': objectif_data['ordre'],
            'actif': True,
        }
    )
    if not created:
        objectif.description = objectif_data['description']
        objectif.icone = objectif_data['icone']
        objectif.ordre_affichage = objectif_data['ordre']
        objectif.actif = True
        objectif.save()
    print(f"OK - Objectif '{objectif_data['titre']}' mis a jour")

# 5. Mettre à jour la présentation dans About
print("\n" + "=" * 60)
print("Informations mises a jour avec succes!")
print("=" * 60)
print("\nVous pouvez maintenant:")
print("1. Modifier la Vision/Mission/Valeurs dans l'admin:")
print("   http://127.0.0.1:8000/admin/core/visionmission/")
print("\n2. Les informations sont maintenant disponibles sur:")
print("   - http://127.0.0.1:8000/a-propos/")
print("   - http://127.0.0.1:8000/vision-mission/")
print("\n3. Pour ajouter les descriptions detailees des services,")
print("   modifiez les contenus dans l'admin pour chaque service.")

