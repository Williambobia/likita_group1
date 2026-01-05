from django.shortcuts import render, get_object_or_404
from .models import Emission, ArticleEmission


def liste_emissions(request):
    """Liste de toutes les émissions"""
    emissions = Emission.objects.filter(publie=True)
    context = {
        'emissions': emissions,
    }
    return render(request, 'media_app/liste_emissions.html', context)


def detail_emission(request, slug):
    """Détail d'une émission"""
    emission = get_object_or_404(Emission, slug=slug, publie=True)
    # Incrémenter les vues
    emission.incrementer_vues()
    articles = emission.articles.filter(publie=True)
    context = {
        'emission': emission,
        'articles': articles,
    }
    return render(request, 'media_app/detail_emission.html', context)

