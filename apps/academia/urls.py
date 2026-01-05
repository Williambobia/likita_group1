from django.urls import path
from . import views

app_name = 'academia'

urlpatterns = [
    path('', views.liste_formations, name='liste_formations'),
    path('mes-formations/', views.mes_formations, name='mes_formations'),
    path('certificat/<int:certificat_id>/telecharger/', views.telecharger_certificat, name='telecharger_certificat'),
    path('<slug:slug>/inscription/', views.inscription_formation, name='inscription_formation'),
    path('<slug:slug>/', views.detail_formation, name='detail_formation'),
]

