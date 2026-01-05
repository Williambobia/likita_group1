from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Article, Categorie, Commentaire


def liste_articles(request):
    """Liste de tous les articles publiés"""
    articles = Article.objects.filter(statut='publie')
    
    # Filtrer par catégorie si demandé
    categorie_slug = request.GET.get('categorie')
    categorie = None
    if categorie_slug:
        categorie = get_object_or_404(Categorie, slug=categorie_slug)
        articles = articles.filter(categorie=categorie)
    
    # Recherche
    recherche = request.GET.get('q')
    if recherche:
        articles = articles.filter(
            models.Q(titre__icontains=recherche) |
            models.Q(description_courte__icontains=recherche) |
            models.Q(contenu__icontains=recherche) |
            models.Q(tags__icontains=recherche)
        )
    
    categories = Categorie.objects.all()
    
    context = {
        'articles': articles,
        'categories': categories,
        'categorie_active': categorie,
        'recherche': recherche,
    }
    return render(request, 'blog/liste_articles.html', context)


def detail_article(request, slug):
    """Détail d'un article"""
    article = get_object_or_404(Article, slug=slug, statut='publie')
    
    # Incrémenter les vues
    article.incrementer_vues()
    
    # Articles similaires (même catégorie)
    articles_similaires = Article.objects.filter(
        categorie=article.categorie,
        statut='publie'
    ).exclude(id=article.id)[:3]
    
    # Commentaires approuvés
    commentaires = article.commentaires.filter(approuve=True)
    
    context = {
        'article': article,
        'articles_similaires': articles_similaires,
        'commentaires': commentaires,
    }
    return render(request, 'blog/detail_article.html', context)


@login_required
def ajouter_commentaire(request, slug):
    """Ajouter un commentaire à un article"""
    article = get_object_or_404(Article, slug=slug, statut='publie')
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu', '').strip()
        if contenu:
            commentaire = Commentaire.objects.create(
                article=article,
                auteur=request.user,
                contenu=contenu,
                approuve=False  # Nécessite modération
            )
            messages.success(request, 'Votre commentaire a été soumis et sera publié après modération.')
        else:
            messages.error(request, 'Le commentaire ne peut pas être vide.')
    
    return redirect('blog:detail_article', slug=slug)

