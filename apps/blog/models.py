from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Categorie(models.Model):
    """Catégories pour les articles de blog"""
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    couleur = models.CharField(max_length=7, default='#007bff', help_text="Code couleur hexadécimal")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Articles de blog / actualités"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('archive', 'Archivé'),
    ]
    
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    description_courte = models.TextField(max_length=500, help_text="Résumé pour les listes")
    contenu = models.TextField()
    image_principale = models.ImageField(upload_to='blog/', blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Tags séparés par des virgules")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    vues = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_publication = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication', '-date_creation']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        if self.statut == 'publie' and not self.date_publication:
            from django.utils import timezone
            self.date_publication = timezone.now()
        super().save(*args, **kwargs)

    def incrementer_vues(self):
        """Incrémenter le compteur de vues"""
        self.vues += 1
        self.save(update_fields=['vues'])

    @property
    def est_publie(self):
        return self.statut == 'publie'


class Commentaire(models.Model):
    """Commentaires sur les articles"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentaires')
    contenu = models.TextField()
    approuve = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.article.titre}"

