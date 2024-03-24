from django.shortcuts import render, get_object_or_404
from .models import Projets, Taches

def liste_projets(request):
    projets = Projets.objects.all()
    return render(request, 'liste_projets.html', {'projets': projets})

def detail_projet(request, projet_id):
    projet = get_object_or_404(Projets, pk=projet_id)
    taches = Taches.objects.filter(projet_id = projet.id_projet)
    return render(request, 'detail_projet.html', {'projet': projet, "taches": taches})
