from django.db import models
from django import forms
from .models import Client,Prevision,PeriodeSemense,Semense, Client 
# Create your models here.
class ClientForm(forms.ModelForm):
    nom = forms.CharField(max_length=200)
    prenom =forms.CharField(max_length=200)
    contact = forms.CharField(max_length=15, unique=True)
    email =  forms.EmailField(max_length=254, unique=True)
    password = forms.CharField(max_length=200) 
    is_admin =  forms.BooleanField(default=False)

class SemenseForm(forms.ModelForm):
    client = forms.ForeignKey(Client, on_delete=forms.CASCADE, related_name="semences")  # ou User
    nom = forms.CharField(max_length=200)
    ville = forms.CharField(max_length=200)
    duree = forms.IntegerField()   
    date = forms.DateField()

class Prevision(forms.ModelForm):
    mois = forms.CharField(max_length=200)
    statut = forms.CharField(max_length=100)
    duree = forms.IntegerField()  
    semense = forms.ForeignKey(Semense, on_delete=forms.CASCADE, related_name="previsions")

class PeriodeSemence(forms.ModelForm):
    client = forms.ForeignKey(Client, on_delete=forms.CASCADE)
    semence = forms.CharField(max_length=100)
    debut = forms.DateField()
    fin = forms.DateField()
    enregistrement = forms.DateTimeField(auto_now_add=True)