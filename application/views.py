from urllib import request
import requests
import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from .models import Semense,Client,DonneeSaison,DonneeJour
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from datetime import date,datetime, timedelta
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, "index.html", get_meteo_context())


def inscript(request):
    if request.method == "POST":
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        contact = request.POST['contact']
        naissance_str = request.POST['naissance']   
        email = request.POST['email'].strip().lower()
        password = make_password(request.POST.get('password'))

        naissance = datetime.strptime(naissance_str, "%Y-%m-%d").date()

        client = Client(
            nom=nom,
            prenom=prenom,
            email=email,
            contact=contact,
            naissance=naissance,
            password=password
        )
        client.save()
        return redirect('connection')
    return render(request, 'inscription.html')

def connect(request):
    if request.method == "POST":
        contact = request.POST.get('contact', '').strip().lower()
        password = request.POST.get('password')

        try:
            client = Client.objects.get(contact=contact)
            if check_password(password, client.password):
                request.session['client_id'] = client.id
                messages.success(request, "Connexion réussie.")
                return redirect('cereale')   
            else:
                messages.error(request, "Mot de passe incorrect.")
                return redirect('connection')

        except Client.DoesNotExist:
            messages.error(request, "Contact introuvable. Créez un compte.")
            return redirect('inscription')
    return render(request, 'connection.html')
 
 
CATEGORIES_SEMENCE = {
    "maïs": "cereal",
    "sorgho": "cereal",
    "riz": "cereal",
    "arachide": "oleagineux",
    "soja": "oleagineux",
    "niébé": "legumineuse",
    "manioc": "legume_racine",
    "igname": "legume_racine",
    "gombo": "legume_feuille",
    "tomate": "legumes_fruit",
    "carotte": "legume_feuille",
    "haricot": "legumineuse",
    "ble": "cereal",
    "pois": "legumineuse",
    "poivron": "legume_fruit",
    "mille": "cereal",
    "feuille": "legume_feuille",
    "legume": "legume_feuille",
    "orange": "fruit",
    "citron": "fruit",
    "pamplemousse": "fruit",
    "mangue": "fruit",
    "avocat": "fruit",
    "piment": "fruit",
    "pomme de terre": "legume_racine",
    "patate douce": "legume_racine",
    "chou": "legume_feuille",
    "fraise": "fruit",
    "framboise": "fruit",
    "mangue": "fruit",
    "pasteque": "fruit",
    "melon": "fruit",
    "pomme": "fruit",
    "banane": "fruit",
    "ananas": "fruit",
    "papaye": "fruit",
    "cacao": "cereal",
}

def renseigne(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if not name:
            messages.error(request, "Le nom de la semence est requis.")
            return render(request, "renseigne.html")

        date = request.POST.get("date")
        mois_str = request.POST.get("mois")
        pays = request.POST.get("pays")
        region = request.POST.get("region")

        try:
            mois = int(mois_str)
        except (ValueError, TypeError):
            messages.error(request, "La durée (mois) est invalide.")
            return render(request, "renseigne.html")

        type_semence = CATEGORIES_SEMENCE.get(name)
        if not type_semence:
            messages.error(request, f"La semence '{name}' n’est pas reconnue.")
            return render(request, "renseigne.html")

        client_id = request.session.get('client_id')
        if not client_id:
            messages.error(request, "Vous devez être connecté pour enregistrer une semence.")
            return redirect("connection")

        client = Client.objects.get(id=client_id)

        Semense.objects.create(
            name=name,
            date=date,
            mois=mois,
            pays=pays,
            region=region,
            type_semence=type_semence,
            client=client
        )

        messages.success(request, "Semence enregistrée avec succès.")
        return redirect("table")

    return render(request, "renseigne.html")


def table(request):
    client_id = request.session.get('client_id')
    if not client_id:
        messages.error(request, "Veuillez vous connecter pour voir vos semences.")
        return redirect("connection")

    semenses = Semense.objects.filter(client_id=client_id)
    return render(request, 'table.html', {'semenses': semenses})

def supprimer_semense(request, id):
    semense = get_object_or_404(Semense, id=id)
    if request.method == "POST":
        semense.delete()
        messages.success(request, "Semence supprimée.")
    return redirect('table')


def utilisateur(request):
    return render(request, 'user.html')

def mais(request):
    return render(request, 'mais.html')

def mill(request):
    return render(request, 'mille.html')

def sorg(request):
    return render(request, 'sorgho.html')

def arachid(request):
    return render(request, 'arachide.html')

def riz(request):
    return render(request, 'riz.html')

def manioc(request):
    return render(request, 'igname.html')

def sod(request):
    return render(request, 'sodja.html')

def har(request):
    return render(request, 'haricot.html')

def serv(request):
    return render(request, 'service.html')

def cont(request):
    return render(request, 'contact.html')

def val(request):
    return render(request, 'valeur.html')

 
def  tom(request):
    return render(request, 'tomate.html')

def  ble(request):
    return render(request, 'ble.html')

def  carotte(request):
    return render(request, 'carotte.html')

def  feuille(request):
    return render(request, 'feuille.html')

def  legume(request):
    return render(request, 'legume.html')

def  cata(request):
    return render(request, 'CathegorieA.html')

def  catb(request):
    return render(request, 'CathegorieB.html')

def  conseil(request):
    return render(request, 'conseil.html')

from datetime import date
from .models import DonneeJour

def get_meteo_context(region="Kara"):
    today = date.today()
    try:
        donnees = DonneeJour.objects.get(region=region, date=today)
        temperature = donnees.temperature
        precipitation = donnees.precipitation
        humidite = donnees.humidite
        vent = donnees.vent
    except DonneeJour.DoesNotExist:
        temperature = 27.5
        precipitation = 2.0
        humidite = 85
        vent = 12

    return {
        "temperature": temperature,
        "precipitation": precipitation,
        "humidite": humidite,
        "vent": vent
    }


def cereal(request):
    return render(request, "cereale.html", get_meteo_context())

def cereal_data(request):
    region = "Kara"
    today = date.today()

    try:
        data = DonneeJour.objects.get(region=region, date=today)
    except DonneeJour.DoesNotExist:
        data = {
            "temperature": 27.5,
            "precipitation": 2.0,
            "humidite": 85,
            "vent": 12
        }
        return JsonResponse(data)

    return JsonResponse({
        "temperature": data.temperature,
        "precipitation": data.precipitation,
        "humidite": data.humidite,
        "vent": data.vent
    })



def confirmation(nom_fichier):
    chemin = os.path.join(settings.BASE_DIR, 'projet_301', 'data', nom_fichier)
    with open(chemin, encoding='utf-8') as f:
        return json.load(f)
    

def evaluer_conditions(region, nom, type_semence, debut, fin,
                       temp_moy, humidite_moy, vent_moy, precipitation_totale, source='reelle'):

    SAISONS_SEMENCE = {
        "cereal": "Mai à Juin ou Août à Octobre",
        "oleagineux": "Mai à Juin",
        "fruit": "Août à Octobre",
        "legume_fruit": "Janvier à Mars ou Septembre à Novembre",
        "legume_feuille": "Août à Octobre",
        "legume_racine": "Août à Octobre",
        "legumineuse": "Mai à Juin"
    }

    if type_semence == "cereal":
        conditions = (
            precipitation_totale >= 3 and
            humidite_moy >= 30 and
            temp_moy <= 30 and
            vent_moy <= 20
        )
    elif type_semence == "legume_fruit":
        conditions = (
            precipitation_totale >= 80 and
            humidite_moy >= 75 and
            temp_moy <= 28 and
            vent_moy <= 18
        )
    elif type_semence == "oleagineux":
        conditions = (
            precipitation_totale >= 90 and
            humidite_moy >= 65 and
            temp_moy <= 32 and
            vent_moy <= 25
        )
    else:
        conditions = (
            precipitation_totale >= 100 and
            humidite_moy >= 75 and
            temp_moy <= 28 and
            vent_moy <= 15
        )

    if conditions:
        message = (
            f"(Source: {source}) La saison est favorable à la semence de {nom} à {region}. "
            f"Période recommandée : du {debut.strftime('%d/%m/%Y')} au {fin.strftime('%d/%m/%Y')}."
        )
        return message, debut, fin
    else:
        saison_attente = SAISONS_SEMENCE.get(type_semence, "Mai à Juin ou Août à Octobre")
        message = (
            f"(Source: {source}) La saison à {region} n’est pas encore propice pour {nom}. "
            f"Vous pouvez attendre la saison {saison_attente}."
        )
        return message, None, None

def traitement(request):
    if request.method == "POST":
        semense_id = request.POST.get("semense_id")
        semense = get_object_or_404(Semense, id=semense_id)

        region = semense.region.strip().title()
        nom = semense.name
        type_semence = semense.type_semence
        date_debut = semense.date
        mois = semense.mois

        message, debut, fin = analyse_hybride(region, nom, type_semence, date_debut, mois)

        context = {
            "region": region,
            "nom": nom,
            "type": type_semence,
            "date": date_debut,
            "mois": mois,
            "message": message,
            "debut": debut,
            "fin": fin
        }
        return render(request, "user.html", context)
    return redirect("table")


def analyse_hybride(region, nom, type_semence, date_debut, mois):
    date_fin = date_debut + timedelta(days=mois * 30)

   
    if getattr(settings, 'USE_JSON_MODE', False):
        try:
            data = confirmation("annee.json") 

            region_data = data.get(region)
            if not region_data:
                return f"Aucune donnée pour la région {region} dans le fichier JSON.", None, None

            
            valeurs = []
            for date_str, valeurs_jour in region_data.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if date_debut <= date_obj <= date_fin:
                    valeurs.append(valeurs_jour)

            if valeurs:
                n = len(valeurs)
                temp_moy = sum(v["temperature"] for v in valeurs) / n
                humidite_moy = sum(v["humidite"] for v in valeurs) / n
                vent_moy = sum(v["vent"] for v in valeurs) / n
                precipitation_totale = sum(v["precipitation"] for v in valeurs)

                return evaluer_conditions(region, nom, type_semence, date_debut, date_fin,
                                          temp_moy, humidite_moy, vent_moy, precipitation_totale, source='json')
            else:
                return "Pas de données journalières JSON pour cette période.", None, None

        except FileNotFoundError:
            return "Fichier annee.json introuvable.", None, None

    else:
        # Mode base de données Django
        donnees = DonneeJour.objects.filter(region=region, date__range=(date_debut, date_fin))
        if donnees.exists():
            n = donnees.count()
            temp_moy = sum(d.temperature for d in donnees) / n
            humidite_moy = sum(d.humidite for d in donnees) / n
            vent_moy = sum(d.vent for d in donnees) / n
            precipitation_totale = sum(d.precipitation for d in donnees)

            return evaluer_conditions(region, nom, type_semence, date_debut, date_fin,
                                      temp_moy, humidite_moy, vent_moy, precipitation_totale, source='reelle')
        else:
            today = timezone.now().date()
            annee = today.year
            try:
                saison = DonneeSaison.objects.get(region=region, annee=annee)
                return evaluer_conditions(region, nom, type_semence, date_debut, date_fin,
                                          saison.temp_moy, saison.humidite_moy, saison.vent_moy, saison.precipitation_totale, source='saison')
            except DonneeSaison.DoesNotExist:
                return "Pas de données disponibles pour cette région et année.", None, None
