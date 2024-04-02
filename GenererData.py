import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaldjango.settings')
django.setup()

from projetmanagement.models import Utilisateur, Projets, Taches


# Function to create random users
def create_users():
    users_data = [
        Utilisateur(username="Astrid", email="astrid@animagourmet.com", password=make_password('password123'),
                    estResponsable=True, estGestionnaire=False),
        Utilisateur(username="Audrey", email="audrey@animagourmet.com", password=make_password('password123'),
                    estResponsable=False, estGestionnaire=True),
        Utilisateur(username="Gaetan", email="gaetan@animagourmet.com", password=make_password('password123'),
                    estResponsable=False, estGestionnaire=False)
    ]
    Utilisateur.objects.bulk_create(users_data)


# Function to create random projects
def create_projects():
    projects_data = [
        Projets(id_projet=1, nom="Project 1", avancement=20.5, statut="En cours", date_debut="2024-04-01", date_fin="2024-04-10", responsable_id=1),
        Projets(id_projet=2, nom="Project 2", avancement=10.2, statut="Planifié",  date_debut="2024-03-15", date_fin="2024-04-04",  responsable_id=1),
        Projets(id_projet=3, nom="Project 3", avancement=50.0, statut="Livré", date_debut="2024-01-01", date_fin="2024-01-16", responsable_id=1),
        Projets(id_projet=4, nom="Project 4", avancement=0, statut="En pause", responsable_id=1 , date_debut="2024-04-01", date_fin="2024-04-05",),
        Projets(id_projet=5, nom="Project 5", avancement=75.3, statut="En cours", responsable_id=1, date_debut="2024-02-15", date_fin="2024-03-16", )
    ]
    Projets.objects.bulk_create(projects_data)


def create_tasks():
    tasks_data = [
        Taches(libelle="Task 1", description="Description for Task 1", niveau_profondeur=1, duree=10, avancement=20.5,
               priorite=2, statut="Planifiée", date_debut="2024-04-01", date_fin="2024-04-10", projet_id=1, gestionnaire_id=2),
        Taches(libelle="Task 2", description="Description for Task 2", niveau_profondeur=1, duree=20, avancement=10.2,
               priorite=1, statut="En cours", date_debut="2024-03-15", date_fin="2024-04-04", projet_id=2, gestionnaire_id=2),
        Taches(libelle="Task 3", description="Description for Task 3", niveau_profondeur=1, duree=15, avancement=50.0,
               priorite=3, statut="Réalisée", date_debut="2024-01-01", date_fin="2024-01-16", projet_id=3, gestionnaire_id=2),
        Taches(libelle="Task 4", description="Description for Task 4", niveau_profondeur=1, duree=5, avancement=0,
               priorite=2, statut="En pause", date_debut="2024-04-01", date_fin="2024-04-05", projet_id=4, gestionnaire_id=2),
        Taches(libelle="Task 5", description="Description for Task 5", niveau_profondeur=1, duree=30, avancement=75.3,
               priorite=1, statut="Validée", date_debut="2024-02-15", date_fin="2024-03-16", projet_id=5, gestionnaire_id=2)
    ]
    Taches.objects.bulk_create(tasks_data)
    utilisateur_3 = Utilisateur.objects.get(id=3)
    for task in tasks_data:
        task.employes.add(utilisateur_3)


if __name__ == "__main__":
    create_users()
    create_projects()
    create_tasks()
    print("Sample data generated successfully!")
