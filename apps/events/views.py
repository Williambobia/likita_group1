from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Evenement, Inscription, GalerieEvenement


def liste_evenements(request):
    """Liste de tous les événements"""
    evenements = Evenement.objects.filter(publie=True)
    
    # Filtrer par type si demandé
    type_filter = request.GET.get('type')
    if type_filter:
        evenements = evenements.filter(type_evenement=type_filter)
    
    # Séparer les événements à venir et passés
    maintenant = timezone.now()
    evenements_a_venir = evenements.filter(date_debut__gte=maintenant)
    evenements_passes = evenements.filter(date_debut__lt=maintenant)
    
    context = {
        'evenements_a_venir': evenements_a_venir,
        'evenements_passes': evenements_passes,
        'type_filter': type_filter,
    }
    return render(request, 'events/liste_evenements.html', context)


def detail_evenement(request, slug):
    """Détail d'un événement"""
    evenement = get_object_or_404(Evenement, slug=slug, publie=True)
    galerie = evenement.galerie.all()
    
    # Vérifier si l'utilisateur est déjà inscrit
    deja_inscrit = False
    inscription = None
    if request.user.is_authenticated:
        inscription = Inscription.objects.filter(
            utilisateur=request.user,
            evenement=evenement
        ).first()
        deja_inscrit = inscription is not None
    
    context = {
        'evenement': evenement,
        'galerie': galerie,
        'deja_inscrit': deja_inscrit,
        'inscription': inscription,
    }
    return render(request, 'events/detail_evenement.html', context)


@login_required
def inscription_evenement(request, slug):
    """Inscription à un événement"""
    evenement = get_object_or_404(Evenement, slug=slug, publie=True)
    
    # Vérifier si déjà inscrit
    inscription_existante = Inscription.objects.filter(
        utilisateur=request.user,
        evenement=evenement
    ).first()
    
    if inscription_existante:
        messages.warning(request, 'Vous êtes déjà inscrit à cet événement.')
        return redirect('events:detail_evenement', slug=slug)
    
    # Vérifier les places disponibles
    if evenement.est_complet:
        messages.error(request, 'Désolé, cet événement est complet.')
        return redirect('events:detail_evenement', slug=slug)
    
    # Créer l'inscription
    inscription = Inscription.objects.create(
        utilisateur=request.user,
        evenement=evenement,
        statut='en_attente'
    )
    
    messages.success(request, f'Votre inscription à "{evenement.titre}" a été enregistrée!')
    return redirect('events:detail_evenement', slug=slug)


@login_required
def mes_inscriptions(request):
    """Liste des inscriptions de l'utilisateur"""
    inscriptions = Inscription.objects.filter(utilisateur=request.user)
    context = {
        'inscriptions': inscriptions,
    }
    return render(request, 'events/mes_inscriptions.html', context)

