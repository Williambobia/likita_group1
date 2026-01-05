"""
Script pour remplir automatiquement la biographie de Nadine Pulumba
Exécutez ce script après avoir créé un MessageDirectrice dans l'admin
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'likita_group.settings')
django.setup()

from apps.core.models import MessageDirectrice

# Informations de Nadine Pulumba
biographie_complete = """Nadine Pulumba est la Directrice Générale de la Société LIKITA Group. 
Passionnée par le journalisme et la communication, elle s'engage activement dans l'autonomisation des femmes 
et le développement communautaire à travers les médias, les événements et l'éducation."""

formation = """Graduée en journalisme et Licenciée en communication stratégique des organisations 
à l'Université des Sciences de l'Information et de la Communication (UNISIC) ex (IFASIC)."""

competences = """• Camerawoman : Réalisation de captations vidéo et de montages, avec une attention 
particulière à la narration visuelle.

• Assistante administrative

• Conférencière : Animatrice d'ateliers et de conférences sur des thématiques telles que le leadership, 
l'empowerment et la communication efficace.

• Maîtresse de Cérémonies : Animation d'événements variés, garantissant une expérience engageante 
et dynamique pour les participants.

• Conseillère en Communication : Accompagnement d'organisations et d'individus dans le développement 
de stratégies de communication efficaces, incluant la rédaction de contenu et la gestion des relations publiques.

Actuellement Journaliste et Présentatrice télé, Nadine Pulumba est passionnée par le journalisme. 
Son expérience inclut la couverture d'événements et de sujets d'actualité, en mettant l'accent sur 
les histoires qui inspirent et éduquent le public. Elle s'efforce de donner une voix à ceux qui 
souvent ne sont pas entendus."""

engagement_communautaire = """• Initiatrice du Forum Mwasi Mwinda : Un événement annuel visant à célébrer 
les contributions et réalisations des femmes dans divers secteurs, tout en favorisant le dialogue et le réseautage.

• Engagement Communautaire : Participation à des initiatives locales pour l'émancipation des femmes 
et le développement communautaire.

• Collaboration avec des ONG et différentes structures pour promouvoir des programmes d'éducation 
et de sensibilisation."""

# Mettre à jour ou créer le message de la directrice
message, created = MessageDirectrice.objects.get_or_create(
    signature="Nadine Pulumba",
    defaults={
        'titre': 'Mot de la Directrice Générale',
        'fonction': 'Directrice Générale de la Société LIKITA Group',
        'actif': True,
        'biographie_complete': biographie_complete,
        'formation': formation,
        'competences': competences,
        'engagement_communautaire': engagement_communautaire,
    }
)

if not created:
    # Mettre à jour les informations existantes
    message.biographie_complete = biographie_complete
    message.formation = formation
    message.competences = competences
    message.engagement_communautaire = engagement_communautaire
    message.save()
    print("OK - Informations de Nadine Pulumba mises a jour avec succes!")
else:
    print("OK - Informations de Nadine Pulumba creees avec succes!")

print(f"\nVous pouvez maintenant modifier ces informations dans l'admin:")
print(f"   http://127.0.0.1:8000/admin/core/messagedirectrice/{message.id}/change/")

