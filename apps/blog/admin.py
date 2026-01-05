from django.contrib import admin
from django.utils.html import format_html
from .models import Categorie, Article, Commentaire


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug', 'date_creation']
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ['nom', 'description']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'titre', 'auteur', 'categorie', 'statut', 'vues', 'date_publication']
    list_filter = ['statut', 'categorie', 'date_publication', 'date_creation']
    search_fields = ['titre', 'description_courte', 'contenu', 'tags']
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'
    ordering = ['-date_publication']
    raw_id_fields = ['auteur', 'categorie']
    readonly_fields = ['vues', 'date_creation', 'date_modification', 'image_preview_large']
    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'slug', 'auteur', 'categorie', 'description_courte', 'contenu', 'image_principale', 'image_preview_large', 'tags')
        }),
        ('Publication', {
            'fields': ('statut', 'date_publication', 'vues')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image_principale:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 5px;" />', obj.image_principale.url)
        return "Pas d'image"
    image_preview.short_description = "Image"
    
    def image_preview_large(self, obj):
        if obj.image_principale:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%; object-fit: contain;" />', obj.image_principale.url)
        return "Aucune image"
    image_preview_large.short_description = "Aperçu"


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ['article', 'auteur', 'approuve', 'date_creation']
    list_filter = ['approuve', 'date_creation']
    search_fields = ['contenu', 'auteur__username', 'article__titre']
    raw_id_fields = ['article', 'auteur']
    date_hierarchy = 'date_creation'

