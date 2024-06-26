from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Projets, Taches, Utilisateur, Dates
from django.http import HttpResponseBadRequest
from django.utils import timezone
from datetime import datetime, date
from django.contrib import messages


@login_required
def liste_projets(request):
    if request.method == 'POST':
        nom_projet = request.POST.get('nom_projet', '')
        if nom_projet:
            date_debut = timezone.now().date()
            date_fin = timezone.now().date()
            projet = Projets.objects.create(nom=nom_projet, avancement=0, statut='Planifié', date_fin=date_fin,
                                            date_debut=date_debut, responsable=request.user)
            messages.success(request, "Le projet a été créé avec succès.")
            return redirect('liste_projets')
        else:
            messages.error(request, "Le nom du projet est vide.")
    projets = {
        'en cours': Projets.objects.filter(statut='En cours'),
        'planifiés': Projets.objects.filter(statut='Planifié'),
        'en pause': Projets.objects.filter(statut='En pause'),
        'livrés': Projets.objects.filter(statut='Livré'),
    }
    return render(request, 'liste_projets.html', {'projets': projets,})


@login_required
def detail_projet(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    utilisateurs = Utilisateur.objects.all()

    for tache in Taches.objects.filter(projet_id=projet.id_projet):
        tache.mettre_a_jour_statut_absence()

    taches_par_statut = {
        'Planifiée': Taches.objects.filter(projet_id=projet.id_projet, statut='Planifiée'),
        'En cours': Taches.objects.filter(projet_id=projet.id_projet, statut='En cours'),
        'Réalisée': Taches.objects.filter(projet_id=projet.id_projet, statut='Réalisée'),
        'En pause': Taches.objects.filter(projet_id=projet.id_projet, statut='En pause'),
        'Validée': Taches.objects.filter(projet_id=projet.id_projet, statut='Validée'),
    }

    return render(request, 'detail_projet.html',
                  {'projet': projet, 'taches_par_statut': taches_par_statut, 'utilisateurs': utilisateurs})


@login_required
def creer_tache(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    utilisateurs = Utilisateur.objects.all()

    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        description = request.POST.get('description')
        priorite = request.POST.get('priorite')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')
        employes_ids = request.POST.getlist('assigne')

        if not all([libelle, description, priorite, date_debut_str, date_fin_str]):
            messages.error(request, "Merci de remplir tous les champs.")
        else:
            try:
                date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
                date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()

                # Vérifie si la date de début est antérieure à la date du jour
                if date_debut < date.today():
                    messages.error(request, "La date de début ne peut pas être antérieure à la date d'aujourd'hui.")

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
                messages.error(request, "Format de date invalide.")

    return render(request, 'create_tache.html', {'utilisateurs': utilisateurs})


@login_required
def supprimer_tache(request, tache_id):
    tache = get_object_or_404(Taches, id_tache=tache_id)
    if request.method == 'POST':
        projet = tache.projet
        tache.delete()

        # recalcul des dates du projet
        taches_projet = Taches.objects.filter(projet=projet)
        if taches_projet.exists():
            projet.date_debut = min(taches_projet.values_list('date_debut', flat=True))
            projet.date_fin = max(taches_projet.values_list('date_fin', flat=True))
        else:
            projet.date_debut = timezone.now()
            projet.date_fin = timezone.now()
            projet.statut = 'En pause'
        projet.save()

        messages.success(request, "La tâche a été supprimée avec succès.")
        return redirect('detail_projet', projet_id=projet.id_projet)

@login_required
def creer_sous_tache(request, tache_id):
    tache_parente = get_object_or_404(Taches, pk=tache_id)
    sous_tache = None
    utilisateurs = Utilisateur.objects.all()

    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        description = request.POST.get('description')
        priorite = request.POST.get('priorite')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')
        employes_ids = request.POST.getlist('assigne')

        if not all([libelle, description, priorite, date_debut_str, date_fin_str]):
            messages.error(request, "Merci de remplir tous les champs.")
        else:
            try:
                date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
                date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()

                if date_debut < tache_parente.date_debut or date_fin > tache_parente.date_fin:
                    messages.error(request,
                                   "Les dates de la sous-tâche doivent être comprises dans celles de la tâche parente.")
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
                messages.error(request, "Format de date invalide.")

    return render(request, 'create_tache.html',
                  {'utilisateurs': utilisateurs, 'sous_tache': sous_tache})


@login_required
def supprimer_projet(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    projet.delete()
    messages.success(request, "Le projet a été supprimé avec succès.")
    return redirect('liste_projets')


@login_required
def modifier_statut_projet(request, projet_id):
    if request.method == 'POST':
        projet = get_object_or_404(Projets, pk=projet_id)
        nouveau_statut = request.POST.get('statut')
        if projet.avancement == 100:
            projet.statut = 'Livré'
            return redirect('liste_projets')
        if nouveau_statut in ['Planifié', 'En cours', 'En pause', 'Livré']:
            projet.statut = nouveau_statut
            projet.save()
            return redirect('liste_projets')


@login_required
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
    return HttpResponseBadRequest("Invalid request test")


@login_required
def modifier_statut_tache(request, tache_id):
    if request.method == 'POST':
        tache = get_object_or_404(Taches, pk=tache_id)
        nouveau_statut = request.POST.get('statut')
        if nouveau_statut in ['Planifiée', 'En cours', 'Réalisée', 'En pause', 'Validée']:
            error = tache.check_statut(nouveau_statut)
            if error:
                messages.error(request, error)
            if tache.avancement == 100:
                tache.statut = 'Réalisée'
            if tache.check_employe():
                messages.error(request, "Impossible de passer la tache en cours sans employés")
            tache.save()
            tache.projet.calculer_avancement_moyen()
            tache.projet.verifier_statut_projet()
            return redirect('detail_projet', projet_id=tache.projet_id)
    return HttpResponseBadRequest("Invalid request")


@login_required
def saisie_absence(request):
    if request.method == 'POST':
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        type_absence = request.POST.get('type')

        if not all([debut, fin, type_absence]):
            messages.error(request, "Merci de remplir tous les champs.")

        try:
            date_debut = datetime.strptime(debut, '%Y-%m-%d').date()
            date_fin = datetime.strptime(fin, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Format de date invalide.")
            return render(request, 'saisie_absence.html')

        if date_debut < datetime.now().date():
            messages.error(request, "La date de début ne peut pas être antérieure à aujourd'hui.")
            return render(request, 'saisie_absence.html')

        absence = Dates.objects.create(
            debut=debut,
            fin=fin,
            type=type_absence,
            utilisateur=Utilisateur.objects.get(username=request.user.username)
        )
        for tache in Taches.objects.all():
            if tache.employes.contains(request.user):
                tache.mettre_a_jour_statut_absence()
        messages.success(request, "Absence enregistré.")
    return render(request, 'saisie_absence.html')


@login_required
def ajouter_employe_tache(request, tache_id):
    if request.method == 'POST':
        tache = get_object_or_404(Taches, pk=tache_id)
        utilisateur_id = request.POST.get('employe')
        utilisateur = get_object_or_404(Utilisateur, pk=utilisateur_id)
        tache.employes.add(utilisateur)
    return redirect('detail_projet', projet_id=tache.projet_id)


@login_required
def supprimer_employe_tache(request, tache_id):
    if request.method == 'POST':
        tache = get_object_or_404(Taches, pk=tache_id)
        utilisateur_id = request.POST.get('employe')
        if utilisateur_id is not None:  # Evite de supprimer un utilisateur qui n'existe pas
            utilisateur = get_object_or_404(Utilisateur, pk=utilisateur_id)
        if tache.employes.contains(
                utilisateur):  # S'il y a bien des employes assignes à la tache, supprimer l'utilisateur
            tache.employes.remove(utilisateur)
        tache.check_employe()
        tache.save()
    return redirect('detail_projet', projet_id=tache.projet_id)
