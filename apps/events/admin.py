from django.contrib import admin
from django.utils.html import format_html
from .models import Evenement, Inscription, GalerieEvenement


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'titre', 'type_evenement', 'date_debut', 'lieu', 'statut', 'places_reservees', 'publie']
    list_filter = ['type_evenement', 'statut', 'publie', 'date_debut']
    search_fields = ['titre', 'description', 'lieu']
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_debut'
    ordering = ['-date_debut']
    readonly_fields = ['places_reservees', 'image_preview_large']
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'slug', 'type_evenement', 'description', 'description_courte', 'image', 'image_preview_large')
        }),
        ('Dates et lieu', {
            'fields': ('date_debut', 'date_fin', 'lieu', 'adresse_complete')
        }),
        ('Tarification et places', {
            'fields': ('prix', 'places_disponibles', 'places_reservees')
        }),
        ('Publication', {
            'fields': ('statut', 'publie')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = "Image"
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%; object-fit: contain;" />', obj.image.url)
        return "Aucune image"
    image_preview_large.short_description = "Aperçu"


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'evenement', 'statut', 'date_inscription', 'present']
    list_filter = ['statut', 'present', 'date_inscription', 'evenement']
    search_fields = ['utilisateur__username', 'utilisateur__email', 'evenement__titre']
    raw_id_fields = ['utilisateur', 'evenement']
    date_hierarchy = 'date_inscription'


@admin.register(GalerieEvenement)
class GalerieEvenementAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'titre', 'evenement', 'pour_carrousel', 'ordre_affichage', 'date_creation']
    list_filter = ['evenement', 'pour_carrousel', 'date_creation']
    search_fields = ['titre', 'evenement__titre']
    ordering = ['-pour_carrousel', 'evenement', 'ordre_affichage', '-date_creation']
    raw_id_fields = ['evenement']
    fieldsets = (
        ('Informations', {
            'fields': ('titre', 'ordre_affichage')
        }),
        ('Association', {
            'fields': ('evenement', 'pour_carrousel'),
            'description': 'Choisir un événement OU cocher "Pour carrousel" pour afficher l\'image dans le carrousel de la page d\'accueil'
        }),
        ('Média', {
            'fields': ('image', 'image_preview_large', 'video', 'video_url')
        }),
    )
    readonly_fields = ['image_preview_large']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = "Photo"
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 400px; max-width: 100%; object-fit: contain; border-radius: 10px;" />', obj.image.url)
        return "Aucune photo"
    image_preview_large.short_description = "Aperçu"

