from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Formation, InscriptionFormation, Certificat


def liste_formations(request):
    """Liste de toutes les formations"""
    formations = Formation.objects.filter(publie=True)
    
    # Filtrer par type si demandé
    type_filter = request.GET.get('type')
    if type_filter:
        formations = formations.filter(type_formation=type_filter)
    
    # Filtrer par niveau si demandé
    niveau_filter = request.GET.get('niveau')
    if niveau_filter:
        formations = formations.filter(niveau=niveau_filter)
    
    context = {
        'formations': formations,
        'type_filter': type_filter,
        'niveau_filter': niveau_filter,
    }
    return render(request, 'academia/liste_formations.html', context)


def detail_formation(request, slug):
    """Détail d'une formation"""
    formation = get_object_or_404(Formation, slug=slug, publie=True)
    
    # Vérifier si l'utilisateur est déjà inscrit
    deja_inscrit = False
    inscription = None
    certificat = None
    if request.user.is_authenticated:
        inscription = InscriptionFormation.objects.filter(
            utilisateur=request.user,
            formation=formation
        ).first()
        deja_inscrit = inscription is not None
        if inscription:
            certificat = getattr(inscription, 'certificat', None)
    
    context = {
        'formation': formation,
        'deja_inscrit': deja_inscrit,
        'inscription': inscription,
        'certificat': certificat,
    }
    return render(request, 'academia/detail_formation.html', context)


@login_required
def inscription_formation(request, slug):
    """Inscription à une formation"""
    formation = get_object_or_404(Formation, slug=slug, publie=True)
    
    # Vérifier si déjà inscrit
    inscription_existante = InscriptionFormation.objects.filter(
        utilisateur=request.user,
        formation=formation
    ).first()
    
    if inscription_existante:
        messages.warning(request, 'Vous êtes déjà inscrit à cette formation.')
        return redirect('academia:detail_formation', slug=slug)
    
    # Vérifier les places disponibles
    if formation.est_complet:
        messages.error(request, 'Désolé, cette formation est complète.')
        return redirect('academia:detail_formation', slug=slug)
    
    # Créer l'inscription
    inscription = InscriptionFormation.objects.create(
        utilisateur=request.user,
        formation=formation,
        statut='en_attente'
    )
    
    messages.success(request, f'Votre inscription à "{formation.titre}" a été enregistrée!')
    return redirect('academia:detail_formation', slug=slug)


@login_required
def mes_formations(request):
    """Liste des formations de l'utilisateur"""
    inscriptions = InscriptionFormation.objects.filter(utilisateur=request.user)
    context = {
        'inscriptions': inscriptions,
    }
    return render(request, 'academia/mes_formations.html', context)


@login_required
def telecharger_certificat(request, certificat_id):
    """Télécharger un certificat"""
    certificat = get_object_or_404(Certificat, id=certificat_id, verifie=True)
    
    # Vérifier que l'utilisateur est le propriétaire
    if certificat.inscription.utilisateur != request.user:
        messages.error(request, "Vous n'avez pas accès à ce certificat.")
        return redirect('academia:mes_formations')
    
    if not certificat.fichier_pdf:
        messages.warning(request, "Le certificat n'est pas encore disponible.")
        return redirect('academia:mes_formations')
    
    from django.http import FileResponse
    return FileResponse(certificat.fichier_pdf.open(), as_attachment=True, filename=f"certificat_{certificat.numero_certificat}.pdf")

