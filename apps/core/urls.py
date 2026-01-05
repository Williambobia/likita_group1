from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.about, name='about'),
    path('message-directrice/', views.message_directrice, name='message_directrice'),
    path('biographie-directrice/', views.biographie_directrice, name='biographie_directrice'),
    path('vision-mission/', views.vision_mission, name='vision_mission'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('galerie-images/', views.galerie_images, name='galerie_images'),
    path('galerie-activites/', views.galerie_activites, name='galerie_activites'),
]

