from django.urls import path
from . import views

app_name = 'media_app'

urlpatterns = [
    path('', views.liste_emissions, name='liste_emissions'),
    path('<slug:slug>/', views.detail_emission, name='detail_emission'),
]

