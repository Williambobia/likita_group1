from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from .models import ProfilUtilisateur


def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer le profil utilisateur
            ProfilUtilisateur.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}!')
            login(request, user)
            # Rediriger les administrateurs vers l'interface admin
            if user.is_staff or user.is_superuser:
                return redirect('admin:index')
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request):
    """Profil de l'utilisateur connecté"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    return render(request, 'users/profile.html')


def logout_view(request):
    """Vue de déconnexion personnalisée - accepte GET et POST"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès. À bientôt !')
    # Rediriger vers la page d'accueil après déconnexion
    return redirect('core:home')


class CustomLoginView(LoginView):
    """Vue de connexion personnalisée qui redirige les admins vers l'interface admin"""
    template_name = 'users/login.html'
    
    def get_success_url(self):
        """Rediriger les administrateurs vers l'interface admin"""
        # Si l'utilisateur est staff ou superuser, rediriger vers l'admin
        if self.request.user.is_staff or self.request.user.is_superuser:
            return reverse('admin:index')
        # Sinon, rediriger vers la page d'accueil
        return reverse('core:home')

