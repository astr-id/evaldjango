from django.urls import path
from . import views

urlpatterns = [
    path('projets/', views.liste_projets, name='liste_projets'),
    path('projet/<int:projet_id>/', views.detail_projet, name='detail_projet'),
    path('projet/<int:projet_id>/creer-tache/', views.creer_tache, name='creer_tache'),
    path('supprimer_projet/<int:projet_id>/', views.supprimer_projet, name='supprimer_projet'),
]
