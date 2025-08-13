from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    naissance = models.DateField()
    contact = models.CharField(max_length=8, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    is_email_generated = models.BooleanField(default=True)
    password = models.CharField(max_length=200)

class Semense(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()   
    mois = models.IntegerField()
    pays = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    type_semence = models.CharField(max_length=50,default='cereal',choices=[
        ('cereal', 'Céréale'),
        ('oleagineux', 'Oléagineux'),
        ('fruit', 'Fruit'),
        ('legume_fruit', 'Légume Fruit'),
        ('legume_feuille', 'Légume Feuille'),
        ('legume_racine', 'Légume Racine'),
        ('legumineuse', 'Légumineuse')
    ])
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='semences', null=True)

class DonneeJour(models.Model):
    region = models.CharField(max_length=50)
    date = models.DateField()
    temperature = models.FloatField()
    humidite = models.FloatField()
    vent = models.FloatField()
    precipitation = models.FloatField()
    
    class Meta:
        unique_together = ('region', 'date')

class DonneeSaison(models.Model):
    region = models.CharField(max_length=50)
    annee = models.IntegerField()
    temp_moy = models.FloatField()
    humidite_moy = models.FloatField()
    vent_moy = models.FloatField()
    precipitation_totale = models.FloatField()

    def __str__(self):
        return f"{self.region} – {self.annee}"
