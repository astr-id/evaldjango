from django.shortcuts import render, get_object_or_404, redirect
from .models import Projets, Taches, Dates
from datetime import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest


def liste_projets(request):
    if request.method == 'POST':
        nom_projet = request.POST.get('nom_projet', '')
        if nom_projet:
            projet = Projets.objects.create(nom=nom_projet, avancement=0, statut='Planifié')
            return redirect('liste_projets')
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


def creer_tache(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        description = request.POST.get('description')
        priorite = request.POST.get('priorite')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')
        super_tache = request.POST.get('super_tache')

        date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
        date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()

        # Calculer la durée
        duree = (date_fin - date_debut).days

        # Calcul du niveau de profondeur
        niveau_profondeur = 1 if super_tache else 0

        date_obj = Dates.objects.create(debut=date_debut, fin=date_fin, type="Dates_tache")

        tache = Taches.objects.create(
            libelle=libelle,
            description=description,
            niveau_profondeur=niveau_profondeur,
            duree=duree,
            avancement=0,
            priorite=priorite,
            statut="Planifiée",
            date_id=date_obj.id_date,
            projet_id=projet.id_projet
        )

        return redirect('detail_projet', projet_id=projet_id)

    return render(request, 'create_tache.html')


def creer_sous_tache(request, tache_id):
    tache_parente = get_object_or_404(Taches, pk=tache_id)
    sous_tache = True  # Vous créez une sous-tâche
    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        description = request.POST.get('description')
        priorite = request.POST.get('priorite')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')

        date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
        date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()

        # Calculer la durée
        duree = (date_fin - date_debut).days

        # Calcul du niveau de profondeur
        niveau_profondeur = tache_parente.niveau_profondeur + 1

        date_obj = Dates.objects.create(debut=date_debut, fin=date_fin, type="Dates_tache")

        sous_tache = Taches.objects.create(
            libelle=libelle,
            description=description,
            niveau_profondeur=niveau_profondeur,
            duree=duree,
            avancement=0,
            priorite=priorite,
            statut="Planifiée",
            date_id=date_obj.id_date,
            projet=tache_parente.projet,
            tache_parent=tache_parente
        )

        return redirect('detail_projet', projet_id=tache_parente.projet_id)

    return render(request, 'create_tache.html', {'sous_tache': sous_tache})


def supprimer_projet(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    projet.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def supprimer_tache(request, tache_id):
    tache = get_object_or_404(Taches, id_tache=tache_id)
    if request.method == 'POST':
        tache.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def modifier_avancement_tache(request, tache_id):
    if request.method == 'POST':
        tache = get_object_or_404(Taches, pk=tache_id)
        nouvel_avancement = request.POST.get('avancement')
        if nouvel_avancement.isdigit() and 0 <= int(nouvel_avancement) <= 100:
            tache.avancement = int(nouvel_avancement)
            tache.save()
            return redirect('detail_projet', projet_id=tache.projet_id)
    return HttpResponseBadRequest("Invalid request")


def modifier_statut_tache(request, tache_id):
    if request.method == 'POST':
        tache = get_object_or_404(Taches, pk=tache_id)
        nouveau_statut = request.POST.get('statut')
        if nouveau_statut in ['Planifiée', 'En cours', 'Réalisée', 'En pause', 'Validée']:
            tache.statut = nouveau_statut
            tache.save()
            return redirect('detail_projet', projet_id=tache.projet_id)
    return HttpResponseBadRequest("Invalid request")
