from django.urls import path
from . import views

urlpatterns = [
    path('projets/', views.liste_projets, name='liste_projets'),
    path('projet/<int:projet_id>/', views.detail_projet, name='detail_projet'),
    path('projet/<int:projet_id>/creer-tache/', views.creer_tache, name='creer_tache'),
    path('supprimer_projet/<int:projet_id>/', views.supprimer_projet, name='supprimer_projet'),
    path('modifier_avancement_tache/<int:tache_id>/', views.modifier_avancement_tache,
         name='modifier_avancement_tache'),
    path('modifier_statut_tache/<int:tache_id>/', views.modifier_statut_tache, name='modifier_statut_tache'),
    path('projet/<int:tache_id>/creer-sous-tache/', views.creer_sous_tache, name='creer_sous_tache'),
    path('supprimer_tache/<int:tache_id>/', views.supprimer_tache, name='supprimer_tache'),
    path('saisie_absence/', views.saisie_absence, name='saisie_absence'),
    path('ajouter_employe_tache/<int:tache_id>/', views.ajouter_employe_tache, name='ajouter_employe_tache'),
    path('supprimer_employe_tache/<int:tache_id>/', views.supprimer_employe_tache, name='supprimer_employe_tache'),
    path('modifier_statut_projet/<int:projet_id>/', views.modifier_statut_projet, name='modifier_statut_projet'),
    path('*', views.homepage)
]
