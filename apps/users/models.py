from django.db import models
from django.contrib.auth.models import User


class ProfilUtilisateur(models.Model):
    """Profil étendu pour les utilisateurs"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profils/', blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil Utilisateur"
        verbose_name_plural = "Profils Utilisateurs"

    def __str__(self):
        return f"Profil de {self.user.username}"

