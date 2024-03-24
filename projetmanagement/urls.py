from django.urls import path
from . import views

urlpatterns = [
    path('projets/', views.liste_projets, name='liste_projets'),
    path('projet/<int:projet_id>/', views.detail_projet, name='detail_projet'),
]
