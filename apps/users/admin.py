from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import ProfilUtilisateur


class ProfilUtilisateurInline(admin.StackedInline):
    model = ProfilUtilisateur
    can_delete = False
    verbose_name_plural = "Profil"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfilUtilisateurInline,)


# Réenregistrer UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ['user', 'telephone', 'profession', 'date_creation']
    search_fields = ['user__username', 'user__email', 'telephone']

