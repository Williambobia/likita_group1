from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from pathlib import Path
import os
from .models import Membre, MessageDirectrice, VisionMission
from apps.events.models import Evenement, GalerieEvenement
from apps.academia.models import Formation
from apps.media_app.models import Emission
from apps.blog.models import Article


def home(request):
    """Page d'accueil"""
    from apps.events.models import GalerieEvenement
    
    # Récupérer les photos pour le carrousel (marquées pour_carrousel=True)
    photos_lancement = list(GalerieEvenement.objects.filter(
        image__isnull=False
    ).exclude(
        image=''
    ).filter(
        pour_carrousel=True
    ).order_by('ordre_affichage', 'date_creation')[:10])
    
    # Récupérer la directrice
    message_directrice = MessageDirectrice.objects.filter(actif=True).first()
    
    # Récupérer les membres (exclure la directrice "Pulumba Nadine" pour éviter les doublons)
    membres = Membre.objects.filter(actif=True).exclude(
        nom__icontains='Pulumba'
    ).exclude(
        prenom__icontains='Nadine'
    )[:6]
    
    # Créer une liste combinée pour l'affichage dans la section équipe
    # La directrice sera affichée en premier si elle a une photo
    membres_avec_directrice = []
    if message_directrice and message_directrice.photo:
        # Créer un objet membre virtuel pour la directrice
        directrice_membre = type('DirectriceMembre', (), {
            'photo': message_directrice.photo,
            'nom_complet': message_directrice.signature,
            'fonction': message_directrice.fonction,
            'biographie': message_directrice.biographie_complete or '',
            'nom': message_directrice.signature.split()[0] if message_directrice.signature else '',
            'prenom': ' '.join(message_directrice.signature.split()[1:]) if len(message_directrice.signature.split()) > 1 else '',
            'is_directrice': True,
        })()
        membres_avec_directrice.append(directrice_membre)
    
    # Ajouter les autres membres
    membres_avec_directrice.extend(list(membres))
    
    context = {
        'message_directrice': message_directrice,
        'membres': membres_avec_directrice,  # Liste avec directrice en premier
        'vision': VisionMission.objects.filter(type='vision', actif=True).first(),
        'mission': VisionMission.objects.filter(type='mission', actif=True).first(),
        'valeurs': VisionMission.objects.filter(type='valeur', actif=True).order_by('ordre_affichage'),
        'photos_lancement': photos_lancement,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """Page À propos de LIKITA Group"""
    from apps.events.models import GalerieEvenement
    
    # Photos du lancement pour la page À propos (images du carrousel)
    photos_lancement = GalerieEvenement.objects.filter(
        image__isnull=False
    ).exclude(
        image=''
    ).filter(
        pour_carrousel=True
    ).order_by('ordre_affichage', 'date_creation')[:8]
    
    # Récupérer la directrice
    message_directrice = MessageDirectrice.objects.filter(actif=True).first()
    
    # Récupérer les membres (exclure la directrice si elle est aussi dans les membres)
    # Exclure "Pulumba" et "Nadine" pour éviter les doublons
    membres = Membre.objects.filter(actif=True).exclude(
        nom__icontains='Pulumba'
    ).exclude(
        prenom__icontains='Nadine'
    )
    
    # Créer une liste combinée pour l'affichage dans la section équipe
    # La directrice sera affichée en premier si elle a une photo
    membres_avec_directrice = []
    if message_directrice and message_directrice.photo:
        # Créer un objet membre virtuel pour la directrice
        directrice_membre = type('DirectriceMembre', (), {
            'photo': message_directrice.photo,
            'nom_complet': message_directrice.signature,
            'fonction': message_directrice.fonction,
            'biographie': message_directrice.biographie_complete or '',
            'nom': message_directrice.signature.split()[0] if message_directrice.signature else '',
            'prenom': ' '.join(message_directrice.signature.split()[1:]) if len(message_directrice.signature.split()) > 1 else '',
            'is_directrice': True,
        })()
        membres_avec_directrice.append(directrice_membre)
    
    # Ajouter les autres membres
    membres_avec_directrice.extend(list(membres))
    
    context = {
        'membres': membres_avec_directrice,  # Liste avec directrice en premier
        'vision': VisionMission.objects.filter(type='vision', actif=True).first(),
        'mission': VisionMission.objects.filter(type='mission', actif=True).first(),
        'valeurs': VisionMission.objects.filter(type='valeur', actif=True).order_by('ordre_affichage'),
        'photos_lancement': photos_lancement,
    }
    return render(request, 'core/about.html', context)


def message_directrice(request):
    """Page avec le message de la Directrice Générale"""
    context = {
        'message': MessageDirectrice.objects.filter(actif=True).first(),
    }
    return render(request, 'core/message_directrice.html', context)


def biographie_directrice(request):
    """Page de biographie détaillée de la Directrice Générale"""
    message = MessageDirectrice.objects.filter(actif=True).first()
    context = {
        'directrice': message,
    }
    return render(request, 'core/biographie_directrice.html', context)


def services(request):
    """Page détaillée des services de LIKITA Group"""
    context = {}
    return render(request, 'core/services.html', context)


def vision_mission(request):
    """Page Vision, Mission et Valeurs"""
    context = {
        'vision': VisionMission.objects.filter(type='vision', actif=True).first(),
        'mission': VisionMission.objects.filter(type='mission', actif=True).first(),
        'valeurs': VisionMission.objects.filter(type='valeur', actif=True).order_by('ordre_affichage'),
    }
    return render(request, 'core/vision_mission.html', context)


def contact(request):
    """Page de contact"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')
        
        # Envoyer l'email (si configuré)
        try:
            send_mail(
                subject=f'Contact LIKITA Group: {sujet}',
                message=f'De: {nom} ({email})\n\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else email,
                recipient_list=[settings.CONTACT_EMAIL if hasattr(settings, 'CONTACT_EMAIL') else 'likitaofficiel@gmail.com'],
                fail_silently=True,
            )
            messages.success(request, 'Votre message a été envoyé avec succès! Nous vous répondrons dans les plus brefs délais.')
        except Exception:
            messages.info(request, 'Votre message a été enregistré. Nous vous répondrons bientôt.')
        
        return redirect('core:contact')
    
    return render(request, 'core/contact.html')


def galerie_activites(request):
    """Page publique de la galerie d'activités et événements"""
    from apps.events.models import GalerieEvenement, Evenement
    
    # Récupérer toutes les images de la galerie d'événements
    # Inclure toutes les photos, même celles du carrousel et sans événement
    galerie_items = GalerieEvenement.objects.filter(
        image__isnull=False
    ).exclude(
        image=''
    ).select_related('evenement').order_by('-date_creation')
    
    # Grouper par événement
    evenements_avec_galerie = {}
    images_sans_evenement = []
    
    for item in galerie_items:
        if item.evenement:  # Si l'image a un événement associé
            evenement_id = item.evenement.id
            if evenement_id not in evenements_avec_galerie:
                evenements_avec_galerie[evenement_id] = {
                    'evenement': item.evenement,
                    'images': []
                }
            evenements_avec_galerie[evenement_id]['images'].append(item)
        else:  # Images sans événement associé
            images_sans_evenement.append(item)
    
    # Si il y a des images sans événement, créer une section "Autres photos"
    if images_sans_evenement:
        evenements_avec_galerie[0] = {
            'evenement': type('Evenement', (), {
                'id': 0,
                'titre': 'Autres Photos',
                'lieu': '',
                'date_debut': None,
            })(),
            'images': images_sans_evenement
        }
    
    # Toutes les images pour la vue mosaïque
    toutes_images = list(galerie_items)
    
    context = {
        'evenements_avec_galerie': evenements_avec_galerie,
        'toutes_images': toutes_images,
        'total_images': len(toutes_images),
    }
    return render(request, 'core/galerie_activites.html', context)


def galerie_images(request):
    """Page galerie avec toutes les images du site"""
    
    images_data = {
        'logos': [],
        'equipe': [],
        'evenements': [],
        'formations': [],
        'emissions': [],
        'blog': [],
        'galerie_evenements': [],
    }
    
    # Logos statiques
    logos_dir = Path(settings.BASE_DIR) / 'static' / 'images' / 'logos'
    if logos_dir.exists():
        for logo_file in logos_dir.glob('*.png'):
            images_data['logos'].append({
                'url': f'/static/images/logos/{logo_file.name}',
                'nom': logo_file.stem,
                'type': 'Logo'
            })
        for logo_file in logos_dir.glob('*.jpg'):
            images_data['logos'].append({
                'url': f'/static/images/logos/{logo_file.name}',
                'nom': logo_file.stem,
                'type': 'Logo'
            })
        for logo_file in logos_dir.glob('*.svg'):
            images_data['logos'].append({
                'url': f'/static/images/logos/{logo_file.name}',
                'nom': logo_file.stem,
                'type': 'Logo'
            })
    
    # Photos de l'équipe
    membres = Membre.objects.filter(actif=True, photo__isnull=False).exclude(photo='')
    for membre in membres:
        if membre.photo:
            images_data['equipe'].append({
                'url': membre.photo.url,
                'nom': f"{membre.nom_complet} - {membre.fonction}",
                'type': 'Équipe',
                'objet': membre
            })
    
    # Photo de la directrice
    message_directrice = MessageDirectrice.objects.filter(actif=True, photo__isnull=False).exclude(photo='').first()
    if message_directrice and message_directrice.photo:
        images_data['equipe'].append({
            'url': message_directrice.photo.url,
            'nom': f"{message_directrice.signature} - {message_directrice.fonction}",
            'type': 'Équipe',
            'objet': message_directrice
        })
    
    # Images des événements
    evenements = Evenement.objects.filter(publie=True, image__isnull=False).exclude(image='')
    for evenement in evenements:
        if evenement.image:
            images_data['evenements'].append({
                'url': evenement.image.url,
                'nom': evenement.titre,
                'type': 'Événement',
                'objet': evenement
            })
    
    # Images de la galerie d'événements (exclure les images du carrousel)
    galerie_items = GalerieEvenement.objects.filter(image__isnull=False).exclude(image='').filter(pour_carrousel=False)
    for item in galerie_items:
        if item.image:
            nom_evenement = item.evenement.titre if item.evenement else "Sans événement"
            images_data['galerie_evenements'].append({
                'url': item.image.url,
                'nom': f"{nom_evenement} - {item.titre or 'Galerie'}",
                'type': 'Galerie Événement',
                'objet': item
            })
    
    # Images des formations
    formations = Formation.objects.filter(publie=True, image__isnull=False).exclude(image='')
    for formation in formations:
        if formation.image:
            images_data['formations'].append({
                'url': formation.image.url,
                'nom': formation.titre,
                'type': 'Formation',
                'objet': formation
            })
    
    # Images des émissions
    emissions = Emission.objects.filter(publie=True, image_thumbnail__isnull=False).exclude(image_thumbnail='')
    for emission in emissions:
        if emission.image_thumbnail:
            images_data['emissions'].append({
                'url': emission.image_thumbnail.url,
                'nom': emission.titre,
                'type': 'Émission',
                'objet': emission
            })
    
    # Images des articles de blog
    articles = Article.objects.filter(statut='publie', image_principale__isnull=False).exclude(image_principale='')
    for article in articles:
        if article.image_principale:
            images_data['blog'].append({
                'url': article.image_principale.url,
                'nom': article.titre,
                'type': 'Article Blog',
                'objet': article
            })
    
    # Compter le total
    total_images = sum(len(images) for images in images_data.values())
    
    context = {
        'images_data': images_data,
        'total_images': total_images,
    }
    
    return render(request, 'core/galerie_images.html', context)

