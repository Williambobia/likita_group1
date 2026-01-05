from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.html import format_html
from django.urls import reverse
from django.conf import settings
from pathlib import Path
from .models import Membre, MessageDirectrice, VisionMission, Logo
from apps.events.models import Evenement, GalerieEvenement
from apps.academia.models import Formation
from apps.media_app.models import Emission
from apps.blog.models import Article


@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ['photo_preview', 'nom', 'prenom', 'fonction', 'ordre_affichage', 'actif']
    list_filter = ['actif', 'fonction']
    search_fields = ['nom', 'prenom', 'fonction']
    ordering = ['ordre_affichage', 'nom']
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'fonction', 'biographie', 'photo')
        }),
        ('Contact', {
            'fields': ('email', 'telephone')
        }),
        ('Affichage', {
            'fields': ('ordre_affichage', 'actif')
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 5px;" />', obj.photo.url)
        return "Pas d'image"
    photo_preview.short_description = "Photo"


@admin.register(MessageDirectrice)
class MessageDirectriceAdmin(admin.ModelAdmin):
    list_display = ['photo_preview', 'titre', 'signature', 'actif', 'date_modification']
    list_filter = ['actif']
    fieldsets = (
        ('Contenu du Message', {
            'fields': ('titre', 'contenu', 'photo', 'photo_preview_large')
        }),
        ('Signature', {
            'fields': ('signature', 'fonction')
        }),
        ('Biographie Complète', {
            'fields': ('biographie_complete', 'formation', 'competences', 'engagement_communautaire'),
            'classes': ('collapse',)
        }),
        ('Publication', {
            'fields': ('actif',)
        }),
    )
    readonly_fields = ['photo_preview_large']
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 5px;" />', obj.photo.url)
        return "Pas d'image"
    photo_preview.short_description = "Photo"
    
    def photo_preview_large(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%; object-fit: contain; border-radius: 10px;" />', obj.photo.url)
        return "Aucune photo"
    photo_preview_large.short_description = "Aperçu"


@admin.register(VisionMission)
class VisionMissionAdmin(admin.ModelAdmin):
    list_display = ['type', 'titre', 'ordre_affichage', 'actif']
    list_filter = ['type', 'actif']
    search_fields = ['titre', 'description']
    ordering = ['type', 'ordre_affichage']


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['logo_preview', 'nom', 'type_logo', 'actif', 'ordre_affichage', 'date_modification']
    list_filter = ['type_logo', 'actif', 'date_creation']
    search_fields = ['nom', 'description']
    ordering = ['type_logo', 'ordre_affichage', 'nom']
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'type_logo', 'description', 'fichier', 'logo_preview_large')
        }),
        ('Affichage', {
            'fields': ('actif', 'ordre_affichage')
        }),
    )
    readonly_fields = ['logo_preview_large']
    
    def logo_preview(self, obj):
        if obj.fichier:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: contain; background: #f0f0f0; padding: 5px; border-radius: 5px;" />', obj.fichier.url)
        return "Pas d'image"
    logo_preview.short_description = "Logo"
    
    def logo_preview_large(self, obj):
        if obj.fichier:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%; object-fit: contain; background: #f0f0f0; padding: 10px; border-radius: 10px;" />', obj.fichier.url)
        return "Aucun logo"
    logo_preview_large.short_description = "Aperçu"


def galerie_images_admin(request):
    """Vue admin pour la galerie d'images"""
    images_data = {
        'logos': [],
        'equipe': [],
        'evenements': [],
        'formations': [],
        'emissions': [],
        'blog': [],
        'galerie_evenements': [],
    }
    
    # Logos depuis le modèle Logo
    logos = Logo.objects.filter(actif=True)
    for logo in logos:
        if logo.fichier:
            images_data['logos'].append({
                'url': logo.fichier.url,
                'nom': logo.nom,
                'type': logo.get_type_logo_display(),
                'objet': logo,
                'objet_type': 'logo'
            })
    
    # Logos statiques (fallback pour les anciens logos non migrés)
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
                'objet': membre,
                'objet_type': 'membre'
            })
    
    # Photo de la directrice
    message_directrice = MessageDirectrice.objects.filter(actif=True, photo__isnull=False).exclude(photo='').first()
    if message_directrice and message_directrice.photo:
        images_data['equipe'].append({
            'url': message_directrice.photo.url,
            'nom': f"{message_directrice.signature} - {message_directrice.fonction}",
            'type': 'Équipe',
            'objet': message_directrice,
            'objet_type': 'messagedirectrice'
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
    
    return render(request, 'admin/galerie_images.html', context)


# Ajouter la vue à l'admin en surchargeant get_urls
original_get_urls = admin.site.get_urls

def custom_get_urls():
    urls = original_get_urls()
    custom_urls = [
        path('galerie-images/', admin.site.admin_view(galerie_images_admin), name='galerie_images'),
    ]
    return custom_urls + urls

admin.site.get_urls = custom_get_urls

