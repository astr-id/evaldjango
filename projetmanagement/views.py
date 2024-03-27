from django.shortcuts import render, get_object_or_404
from .models import Projets, Taches


def liste_projets(request):
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
