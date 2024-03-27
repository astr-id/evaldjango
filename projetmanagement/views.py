from django.shortcuts import render, get_object_or_404, redirect
from .models import Projets, Taches, Dates
from datetime import datetime
from django.http import HttpResponseRedirect

def liste_projets(request):
    if request.method == 'POST':
        nom_projet = request.POST.get('nom_projet', '')
        if nom_projet:
            projet = Projets.objects.create(nom=nom_projet, avancement=0, statut='Planifié')
            return redirect('liste_projets')  # Rediriger vers la même page après la création
    projets = {
        'en cours': Projets.objects.filter(statut='En cours'),
        'planifiés': Projets.objects.filter(statut='Planifié'),
        'en pause': Projets.objects.filter(statut='En pause'),
        'livrés': Projets.objects.filter(statut='Livré'),
    }
    return render(request, 'liste_projets.html', {'projets': projets})


def detail_projet(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    taches_par_statut = {
        'Planifiée': Taches.objects.filter(projet_id=projet.id_projet, statut='Planifiée'),
        'En cours': Taches.objects.filter(projet_id=projet.id_projet, statut='En cours'),
        'Réalisée': Taches.objects.filter(projet_id=projet.id_projet, statut='Réalisée'),
        'En pause': Taches.objects.filter(projet_id=projet.id_projet, statut='En pause'),
        'Validée': Taches.objects.filter(projet_id=projet.id_projet, statut='Validée'),
    }

    return render(request, 'detail_projet.html', {'projet': projet, 'taches_par_statut': taches_par_statut})


def create_projet(request):
    return render(request, 'create_projet.html')


def creer_tache(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        description = request.POST.get('description')
        priorite = request.POST.get('priorite')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')
        super_tache = request.POST.get('super_tache')

        # Convertir les chaînes de date en objets datetime
        date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
        date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()

        # Calculer la durée
        duree = (date_fin - date_debut).days

        # Calcul du niveau de profondeur
        niveau_profondeur = 1 if super_tache else 0

        # Création de l'objet Dates
        date_obj = Dates.objects.create(debut=date_debut, fin=date_fin, type="Dates_tache")

        # Création de l'objet Taches avec la référence à l'objet Dates
        tache = Taches.objects.create(
            libelle=libelle,
            description=description,
            niveau_profondeur=niveau_profondeur,
            duree=duree,
            avancement=0,
            priorite=priorite,
            statut="Planifiée",
            date_id=date_obj.id_date,  # Using the id_date field of Dates
            projet_id=projet.id_projet
        )

        # Redirection vers la page de détail du projet
        return redirect('detail_projet', projet_id=projet_id)

    return render(request, 'create_tache.html')

def supprimer_projet(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    projet.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
