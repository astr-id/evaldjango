import os
import random
from django.utils import timezone
from faker import Faker
from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evaldjango.settings")
import django

django.setup()

from projetmanagement.models import Utilisateur, Dates, Projets, Taches

fake = Faker()

# Function to create random users
def create_users(num_users=10):
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = make_password('password123')  # Default password for all users
        est_responsable = fake.boolean()
        est_gestionnaire = fake.boolean()
        user = Utilisateur.objects.create(username=username, email=email, password=password,
                                           estResponsable=est_responsable, estGestionnaire=est_gestionnaire)
        user.save()

# Function to create random dates
def create_dates(num_dates=10):
    for _ in range(num_dates):
        debut = fake.date_this_decade()
        fin = debut + timezone.timedelta(days=random.randint(1, 30))
        date_type = fake.word()
        date = Dates.objects.create(debut=debut, fin=fin, type=date_type)
        date.save()

# Function to create random projects
def create_projects(num_projects=10):
    for _ in range(num_projects):
        nom = fake.word()
        avancement = random.uniform(0, 100)
        statut = random.choice(['En pause', 'Planifié', 'En cours', 'Livré'])
        responsable = random.choice(Utilisateur.objects.all())
        date = random.choice(Dates.objects.all())
        projet = Projets.objects.create(nom=nom, avancement=avancement, statut=statut, responsable=responsable,
                                         date=date)
        projet.save()

# Function to create random tasks
def create_tasks(num_tasks=10):
    for _ in range(num_tasks):
        libelle = fake.sentence()
        description = fake.paragraph()
        niveau_profondeur = random.randint(1, 5)
        duree = random.randint(1, 100)
        avancement = random.uniform(0, 100)
        priorite = random.randint(1, 3)
        statut = random.choice(['Planifiée', 'En cours', 'Réalisée', 'En pause', 'Validée'])
        gestionnaire = random.choice(Utilisateur.objects.all())
        date = random.choice(Dates.objects.all())
        projet = random.choice(Projets.objects.all())
        tache_parent = random.choice(Taches.objects.all()) if Taches.objects.exists() else None
        task = Taches.objects.create(libelle=libelle, description=description, niveau_profondeur=niveau_profondeur,
                                      duree=duree, avancement=avancement, priorite=priorite, statut=statut,
                                      gestionnaire=gestionnaire, date=date, projet=projet, tache_parent=tache_parent)
        task.save()

if __name__ == "__main__":
    # Adjust the number of objects you want to create
    create_users(5)
    create_dates(5)
    create_projects(5)
    create_tasks(5)
    print("Sample data generated successfully!")
