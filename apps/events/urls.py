from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.liste_evenements, name='liste_evenements'),
    path('mes-inscriptions/', views.mes_inscriptions, name='mes_inscriptions'),
    path('<slug:slug>/inscription/', views.inscription_evenement, name='inscription_evenement'),
    path('<slug:slug>/', views.detail_evenement, name='detail_evenement'),
]

