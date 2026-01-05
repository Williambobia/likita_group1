from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.liste_articles, name='liste_articles'),
    path('<slug:slug>/', views.detail_article, name='detail_article'),
    path('<slug:slug>/commenter/', views.ajouter_commentaire, name='ajouter_commentaire'),
]

