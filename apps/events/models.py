from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Evenement(models.Model):
    """Modèle pour les événements (Likita Events + Forum Mwasi Mwinda)"""
    TYPE_CHOICES = [
        ('forum', 'Forum Mwasi Mwinda'),
        ('conference', 'Conférence'),
        ('atelier', 'Atelier'),
        ('seminaire', 'Séminaire'),
        ('autre', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('a_venir', 'À venir'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    type_evenement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    description_courte = models.TextField(max_length=500, blank=True, help_text="Description courte pour les listes")
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(blank=True, null=True)
    lieu = models.CharField(max_length=200)
    adresse_complete = models.TextField(blank=True)
    image = models.ImageField(upload_to='evenements/', blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Prix en francs congolais")
    places_disponibles = models.IntegerField(default=0, help_text="0 = illimité")
    places_reservees = models.IntegerField(default=0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_venir')
    publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.titre} ({self.get_type_evenement_display()})"

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


class Inscription(models.Model):
    """Inscriptions aux événements"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscriptions')
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='inscriptions')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_confirmation = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, help_text="Notes additionnelles")
    present = models.BooleanField(default=False, help_text="Présent à l'événement")

    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
        unique_together = ['utilisateur', 'evenement']
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.evenement.titre}"

    def save(self, *args, **kwargs):
        # Si c'est une nouvelle inscription et que le statut est confirmé
        if not self.pk and self.statut == 'confirme':
            from django.utils import timezone
            self.date_confirmation = timezone.now()
            # Incrémenter les places réservées
            self.evenement.places_reservees += 1
            self.evenement.save(update_fields=['places_reservees'])
        super().save(*args, **kwargs)


class GalerieEvenement(models.Model):
    """Galerie photo/vidéo pour les événements"""
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='galerie', blank=True, null=True, help_text="Laisser vide pour les images du carrousel")
    titre = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='evenements/galerie/', blank=True, null=True)
    video = models.FileField(upload_to='evenements/galerie/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="URL YouTube, Vimeo, etc.")
    pour_carrousel = models.BooleanField(default=False, help_text="Cocher pour afficher cette image dans le carrousel de la page d'accueil")
    ordre_affichage = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Média de galerie"
        verbose_name_plural = "Galerie d'événements"
        ordering = ['evenement', 'ordre_affichage', '-date_creation']

    def __str__(self):
        if self.evenement:
            return f"{self.evenement.titre} - {self.titre or 'Média'}"
        elif self.pour_carrousel:
            return f"Carrousel - {self.titre or 'Média'}"
        else:
            return f"{self.titre or 'Média'}"

