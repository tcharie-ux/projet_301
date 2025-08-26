from django.urls import path
from . import views
from django.urls import path, include
 
urlpatterns=[
path('', views.redirect_to_index),  # Redirect root URL to /index/
path('index/', views.index, name='index'),

path('inscription/', views.inscript, name='inscription'),

path('connection/', views.connect, name='connection'),

path('services/', views.serv, name='service'),

path('contact/', views.cont, name='contact'),

path('dashboard/', views.cereal, name='cereale'),

path('formulaire/', views.renseigne, name='renseigne'),

path('prediction/', views.utilisateur, name='user'),

path('methode/mais/', views.mais, name='mais'),

path('methode/mil/', views.mill, name='mille'),

path('methode/sorgho/', views.sorg, name='sorgho'),

path('methode/arachide/', views.arachid, name='arachide'),

path('methode/riz/', views.riz, name='riz'),

path('methode/sodja/', views.sod, name='sodja'),

path('methode/igname/', views.manioc, name='igname'),

path('methode/haricot/', views.har, name='haricot'),

path('methode/tomate/', views.tom, name='tomate'),

path('methode/ble/', views.ble, name='ble'),

path('methode/carotte/', views.carotte, name='carotte'),

path('methode/feuille/', views.feuille, name='poivron'),

path('methode/legume/', views.legume, name='legume'),

path('fruit1/', views.cata, name='cathegoriea'),

path('fruit2/', views.catb, name='cathegorieb'),

path('historique/', views.table, name='table'),

path('traitement/', views.traitement, name='traitement'),

path('confirmation/', views.confirmation, name='confirmation'),

path('supprimer/<int:id>/', views.supprimer_semense, name='supprimer_semense'),

]

  