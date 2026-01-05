from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Formation(models.Model):
    """Modèle pour les formations LIKITA Academia"""
    TYPE_CHOICES = [
        ('formation', 'Formation'),
        ('webinaire', 'Webinaire'),
        ('cours', 'Cours en ligne'),
        ('atelier', 'Atelier'),
    ]
    
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('tous', 'Tous niveaux'),
    ]
    
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    theme = models.CharField(max_length=150)
    description = models.TextField()
    description_courte = models.TextField(max_length=500, blank=True)
    type_formation = models.CharField(max_length=20, choices=TYPE_CHOICES, default='formation')
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES, default='tous')
    duree = models.CharField(max_length=50, help_text="Ex: 2 jours, 3 semaines, 20 heures")
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Prix en francs congolais")
    certificat = models.BooleanField(default=False, help_text="Délivre un certificat à la fin")
    image = models.ImageField(upload_to='formations/', blank=True, null=True)
    formateur = models.CharField(max_length=200, blank=True)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    places_disponibles = models.IntegerField(default=0, help_text="0 = illimité")
    places_reservees = models.IntegerField(default=0)
    publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} ({self.get_type_formation_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    @property
    def places_restantes(self):
        if self.places_disponibles == 0:
            return "Illimité"
        return max(0, self.places_disponibles - self.places_reservees)

    @property
    def est_complet(self):
        if self.places_disponibles == 0:
            return False
        return self.places_reservees >= self.places_disponibles


class InscriptionFormation(models.Model):
    """Inscriptions aux formations"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscriptions_formation')
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='inscriptions')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_confirmation = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)
    present = models.BooleanField(default=False, help_text="A suivi la formation")

    class Meta:
        verbose_name = "Inscription Formation"
        verbose_name_plural = "Inscriptions Formations"
        unique_together = ['utilisateur', 'formation']
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.formation.titre}"

    def save(self, *args, **kwargs):
        if not self.pk and self.statut == 'confirme':
            from django.utils import timezone
            self.date_confirmation = timezone.now()
            self.formation.places_reservees += 1
            self.formation.save(update_fields=['places_reservees'])
        super().save(*args, **kwargs)


class Certificat(models.Model):
    """Certificats délivrés aux participants"""
    inscription = models.OneToOneField(InscriptionFormation, on_delete=models.CASCADE, related_name='certificat')
    numero_certificat = models.CharField(max_length=100, unique=True)
    date_delivrance = models.DateTimeField(auto_now_add=True)
    fichier_pdf = models.FileField(upload_to='certificats/', blank=True, null=True)
    verifie = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Certificat"
        verbose_name_plural = "Certificats"
        ordering = ['-date_delivrance']

    def __str__(self):
        return f"Certificat {self.numero_certificat} - {self.inscription.utilisateur.username}"

    def save(self, *args, **kwargs):
        if not self.numero_certificat:
            import uuid
            self.numero_certificat = f"CERT-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

