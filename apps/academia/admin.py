from django.contrib import admin
from django.utils.html import format_html
from .models import Formation, InscriptionFormation, Certificat


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'titre', 'type_formation', 'niveau', 'prix', 'certificat', 'places_reservees', 'publie']
    list_filter = ['type_formation', 'niveau', 'certificat', 'publie', 'date_creation']
    search_fields = ['titre', 'theme', 'description', 'formateur']
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_creation'
    ordering = ['-date_creation']
    readonly_fields = ['places_reservees', 'image_preview_large']
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'slug', 'theme', 'description', 'description_courte', 'image', 'image_preview_large')
        }),
        ('Détails de la formation', {
            'fields': ('type_formation', 'niveau', 'duree', 'formateur', 'certificat')
        }),
        ('Tarification et places', {
            'fields': ('prix', 'places_disponibles', 'places_reservees')
        }),
        ('Dates', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Publication', {
            'fields': ('publie',)
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


@admin.register(InscriptionFormation)
class InscriptionFormationAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'formation', 'statut', 'date_inscription', 'present']
    list_filter = ['statut', 'present', 'date_inscription', 'formation']
    search_fields = ['utilisateur__username', 'utilisateur__email', 'formation__titre']
    raw_id_fields = ['utilisateur', 'formation']
    date_hierarchy = 'date_inscription'


@admin.register(Certificat)
class CertificatAdmin(admin.ModelAdmin):
    list_display = ['numero_certificat', 'inscription', 'date_delivrance', 'verifie']
    list_filter = ['verifie', 'date_delivrance']
    search_fields = ['numero_certificat', 'inscription__utilisateur__username', 'inscription__formation__titre']
    raw_id_fields = ['inscription']
    date_hierarchy = 'date_delivrance'
    readonly_fields = ['numero_certificat', 'date_delivrance']

