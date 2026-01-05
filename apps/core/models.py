from django.db import models
from django.utils.text import slugify


class Membre(models.Model):
    """Modèle pour les membres de l'équipe LIKITA Group"""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True)
    fonction = models.CharField(max_length=150)
    biographie = models.TextField()
    photo = models.ImageField(upload_to='equipe/', blank=True, null=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    ordre_affichage = models.IntegerField(default=0, help_text="Ordre d'affichage (plus petit = en premier)")
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ['ordre_affichage', 'nom']

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.fonction}"

    @property
    def nom_complet(self):
        return f"{self.nom} {self.prenom}".strip()


class MessageDirectrice(models.Model):
    """Message de la Directrice Générale"""
    titre = models.CharField(max_length=200, default="Mot de la Directrice Générale")
    contenu = models.TextField()
    photo = models.ImageField(upload_to='directrice/', blank=True, null=True)
    signature = models.CharField(max_length=200, default="Nadine Pulumba")
    fonction = models.CharField(max_length=200, default="Directrice Générale")
    
    # Informations biographiques détaillées
    biographie_complete = models.TextField(blank=True, help_text="Biographie complète de la directrice")
    formation = models.TextField(blank=True, help_text="Formation académique")
    competences = models.TextField(blank=True, help_text="Compétences et expériences professionnelles")
    engagement_communautaire = models.TextField(blank=True, help_text="Engagement communautaire et initiatives")
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Message de la Directrice"
        verbose_name_plural = "Messages de la Directrice"

    def __str__(self):
        return self.titre


class VisionMission(models.Model):
    """Vision, Mission et Valeurs de LIKITA Group"""
    TYPE_CHOICES = [
        ('vision', 'Vision'),
        ('mission', 'Mission'),
        ('valeur', 'Valeur'),
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    icone = models.CharField(max_length=100, blank=True, help_text="Classe CSS pour l'icône (ex: fa-heart)")
    ordre_affichage = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vision/Mission/Valeur"
        verbose_name_plural = "Vision/Mission/Valeurs"
        ordering = ['type', 'ordre_affichage']

    def __str__(self):
        return f"{self.get_type_display()}: {self.titre}"


class Logo(models.Model):
    """Modèle pour gérer les logos de LIKITA Group"""
    TYPE_CHOICES = [
        ('principal', 'Logo Principal'),
        ('footer', 'Logo Footer'),
        ('favicon', 'Favicon'),
        ('white', 'Logo Blanc'),
        ('dark', 'Logo Sombre'),
        ('autre', 'Autre'),
    ]
    
    nom = models.CharField(max_length=200, help_text="Nom du logo (ex: Logo principal LIKITA)")
    type_logo = models.CharField(max_length=20, choices=TYPE_CHOICES, default='principal', help_text="Type d'utilisation du logo")
    fichier = models.ImageField(upload_to='logos/', help_text="Image du logo (PNG recommandé avec fond transparent)")
    description = models.TextField(blank=True, help_text="Description du logo")
    actif = models.BooleanField(default=True, help_text="Logo actif (sera utilisé sur le site)")
    ordre_affichage = models.IntegerField(default=0, help_text="Ordre d'affichage (plus petit = en premier)")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "Logos"
        ordering = ['type_logo', 'ordre_affichage', 'nom']

    def __str__(self):
        return f"{self.get_type_logo_display()}: {self.nom}"
    
    def save(self, *args, **kwargs):
        # Désactiver les autres logos du même type si celui-ci est actif
        if self.actif:
            Logo.objects.filter(type_logo=self.type_logo, actif=True).exclude(pk=self.pk).update(actif=False)
        super().save(*args, **kwargs)
