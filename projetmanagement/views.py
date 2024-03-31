from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Projets, Taches, Utilisateur
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.utils import timezone
from datetime import datetime, date

@login_required
def liste_projets(request):
    if request.method == 'POST':
        nom_projet = request.POST.get('nom_projet', '')
        if nom_projet:
            date_debut = timezone.now().date()
            date_fin = timezone.now().date()
            projet = Projets.objects.create(nom=nom_projet, avancement=0, statut='Planifié', date_fin=date_fin,
                                            date_debut=date_debut, responsable=request.user)
            return redirect('liste_projets')
    projets = {
        'en cours': Projets.objects.filter(statut='En cours'),
        'planifiés': Projets.objects.filter(statut='Planifié'),
        'en pause': Projets.objects.filter(statut='En pause'),
        'livrés': Projets.objects.filter(statut='Livré'),
    }
    return render(request, 'liste_projets.html', {'projets': projets})

@login_required
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
    error_message = None
    utilisateurs = Utilisateur.objects.all()

    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        description = request.POST.get('description')
        priorite = request.POST.get('priorite')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')
        employes_ids = request.POST.getlist('assigne')

        if not all([libelle, description, priorite, date_debut_str, date_fin_str]):
            error_message = "Merci de remplir tous les champs."
        else:
            try:
                date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
                date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()

                # Vérifie si la date de début est antérieure à la date du jour
                if date_debut < date.today():
                    error_message = "La date de début ne peut pas être antérieure à la date d'aujourd'hui."

                # Calculer la durée
                duree = (date_fin - date_debut).days

                # Calcul du niveau de profondeur
                niveau_profondeur = 0

                tache = Taches.objects.create(
                    libelle=libelle,
                    description=description,
                    niveau_profondeur=niveau_profondeur,
                    duree=duree,
                    avancement=0,
                    priorite=priorite,
                    statut="Planifiée",
                    date_fin=date_fin,
                    date_debut=date_debut,
                    projet=projet,
                    gestionnaire=request.user,
                )

                tache.employes.set(employes_ids)

                # Met à jour les dates du projet si besoin
                if date_debut < projet.date_debut or projet.date_debut is None:
                    projet.date_debut = date_debut
                if date_fin > projet.date_fin or projet.date_fin is None:
                    projet.date_fin = date_fin
                projet.save()

                return redirect('detail_projet', projet_id=projet_id)

            except ValueError:
                error_message = "Format de date invalide."

    return render(request, 'create_tache.html', {'utilisateurs': utilisateurs, 'error_message': error_message})


def supprimer_tache(request, tache_id):
    tache = get_object_or_404(Taches, id_tache=tache_id)
    if request.method == 'POST':
        projet = tache.projet
        tache.delete()

        # recacul dates du projet
        taches_projet = Taches.objects.filter(projet=projet)
        if taches_projet.exists():
            projet.date_debut = min(taches_projet.values_list('date_debut', flat=True))
            projet.date_fin = max(taches_projet.values_list('date_fin', flat=True))
        else:
            projet.date_debut = timezone.now()
            projet.date_fin = None
        projet.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def creer_sous_tache(request, tache_id):
    tache_parente = get_object_or_404(Taches, pk=tache_id)
    sous_tache = None
    error_message = None
    utilisateurs = Utilisateur.objects.all()

    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        description = request.POST.get('description')
        priorite = request.POST.get('priorite')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')
        employes_ids = request.POST.getlist('assigne')

        if not all([libelle, description, priorite, date_debut_str, date_fin_str]):
            error_message = "Merci de remplir tous les champs."
        else:
            try:
                date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
                date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()

                if date_debut < tache_parente.date_debut or date_fin > tache_parente.date_fin:
                    error_message = "Les dates de la sous-tâche doivent être comprises dans celles de la tâche parente."
                else:
                    # Calcul la durée
                    duree = (date_fin - date_debut).days

                    # Calcul du niveau de profondeur
                    niveau_profondeur = tache_parente.niveau_profondeur + 1

                    sous_tache = Taches.objects.create(
                        libelle=libelle,
                        description=description,
                        niveau_profondeur=niveau_profondeur,
                        duree=duree,
                        avancement=0,
                        priorite=priorite,
                        statut="Planifiée",
                        date_fin=date_fin,
                        date_debut=date_debut,
                        projet=tache_parente.projet,
                        tache_parent=tache_parente,
                        gestionnaire=request.user
                    )
                    sous_tache.employes.add(*employes_ids)

                    return redirect('detail_projet', projet_id=tache_parente.projet_id)

            except ValueError:
                error_message = "Format de date invalide."

    return render(request, 'create_tache.html',
                  {'utilisateurs': utilisateurs, 'sous_tache': sous_tache, 'error_message': error_message})

#Suppression d'un projet
def supprimer_projet(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    projet.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))#Permet de rester sur la même page


def modifier_avancement_tache(request, tache_id):
    if request.method == 'POST':
        tache = get_object_or_404(Taches, pk=tache_id)
        nouvel_avancement = request.POST.get('avancement')
        if nouvel_avancement.isdigit() and 0 <= int(nouvel_avancement) <= 100:
            tache.avancement = int(nouvel_avancement)
            if tache.avancement == 100:
                tache.statut = 'Validée'
            tache.save()
            tache.projet.calculer_avancement_moyen()
            tache.projet.verifier_statut_projet()
            return redirect('detail_projet', projet_id=tache.projet_id)
    return HttpResponseBadRequest("Invalid request")


def modifier_statut_tache(request, tache_id):
    if request.method == 'POST':
        tache = get_object_or_404(Taches, pk=tache_id)
        nouveau_statut = request.POST.get('statut')
        if nouveau_statut in ['Planifiée', 'En cours', 'Réalisée', 'En pause', 'Validée']:
            tache.statut = nouveau_statut
            if tache.avancement == 100:
                tache.statut = 'Réalisée'
            tache.save()
            tache.projet.calculer_avancement_moyen()
            tache.projet.verifier_statut_projet()
            return redirect('detail_projet', projet_id=tache.projet_id)
    return HttpResponseBadRequest("Invalid request")
