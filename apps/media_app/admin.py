from django.contrib import admin
from django.utils.html import format_html
from .models import Emission, ArticleEmission


@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'titre', 'date_diffusion', 'invite', 'vues', 'publie']
    list_filter = ['publie', 'date_diffusion']
    search_fields = ['titre', 'description', 'invite']
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_diffusion'
    ordering = ['-date_diffusion']
    readonly_fields = ['image_preview_large']
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'slug', 'description', 'image_thumbnail', 'image_preview_large')
        }),
        ('Média', {
            'fields': ('video', 'video_url', 'duree')
        }),
        ('Détails', {
            'fields': ('date_diffusion', 'invite', 'tags', 'vues')
        }),
        ('Publication', {
            'fields': ('publie',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image_thumbnail:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 5px;" />', obj.image_thumbnail.url)
        return "Pas d'image"
    image_preview.short_description = "Image"
    
    def image_preview_large(self, obj):
        if obj.image_thumbnail:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%; object-fit: contain;" />', obj.image_thumbnail.url)
        return "Aucune image"
    image_preview_large.short_description = "Aperçu"


@admin.register(ArticleEmission)
class ArticleEmissionAdmin(admin.ModelAdmin):
    list_display = ['titre', 'emission', 'auteur', 'publie', 'date_creation']
    list_filter = ['publie', 'date_creation']
    search_fields = ['titre', 'contenu']
    raw_id_fields = ['emission', 'auteur']

