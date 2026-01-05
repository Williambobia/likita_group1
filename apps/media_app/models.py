from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Emission(models.Model):
    """Modèle pour les émissions LIKITA"""
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    video = models.FileField(upload_to='emissions/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="URL YouTube, Vimeo, etc.")
    image_thumbnail = models.ImageField(upload_to='emissions/thumbnails/', blank=True, null=True)
    date_diffusion = models.DateField()
    duree = models.CharField(max_length=20, blank=True, help_text="Ex: 45 min")
    invite = models.CharField(max_length=200, blank=True, help_text="Nom de l'invité(e)")
    tags = models.CharField(max_length=500, blank=True, help_text="Tags séparés par des virgules")
    vues = models.IntegerField(default=0)
    publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Émission"
        verbose_name_plural = "Émissions"
        ordering = ['-date_diffusion', '-date_creation']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def incrementer_vues(self):
        """Incrémenter le compteur de vues"""
        self.vues += 1
        self.save(update_fields=['vues'])


class ArticleEmission(models.Model):
    """Articles liés aux émissions"""
    emission = models.ForeignKey(Emission, on_delete=models.CASCADE, related_name='articles')
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='emissions/articles/', blank=True, null=True)
    publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article d'émission"
        verbose_name_plural = "Articles d'émission"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.emission.titre}"

