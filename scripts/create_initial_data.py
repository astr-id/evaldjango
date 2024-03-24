import os
import django

# Configurez les paramètres de l'application Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaldjango.settings')
django.setup()

# Importez les modèles
from projetmanagement.models import Utilisateur, Dates, Projets, Taches

def create_initial_data():
    # Créez des instances pour chaque modèle avec des données fictives
    utilisateurs = [
        Utilisateur(id_utilisateur=1, nom='Dupont', role='Employé', prenom='Jean'),
        Utilisateur(id_utilisateur=2, nom='Durand', role='Responsable', prenom='Marie'),
        Utilisateur(id_utilisateur=3, nom='Martin', role='Gestionnaire', prenom='Pierre'),
    ]
    Utilisateur.objects.bulk_create(utilisateurs)

    dates = [
        Dates(id_date=1, debut='2024-03-01', fin='2024-03-15', type='Congés'),
        Dates(id_date=2, debut='2024-04-01', fin='2024-04-30', type='Formation'),
        Dates(id_date=3, debut='2024-05-01', fin='2024-05-10', type='Projet'),
    ]
    Dates.objects.bulk_create(dates)

    projets = [
        Projets(id_projet=1, nom='Projet A', avancement=75.50, statut='En cours', utilisateur_id=1, date_id=3),
        Projets(id_projet=2, nom='Projet B', avancement=100.00, statut='Livré', utilisateur_id=2, date_id=3),
        Projets(id_projet=3, nom='Projet C', avancement=40.00, statut='En cours', utilisateur_id=3, date_id=1),
    ]
    Projets.objects.bulk_create(projets)

    taches = [
        Taches(id_tache=1, libelle='Tache A', description='Réaliser la documentation', niveau_profondeur=1, duree=5, avancement=100.00, priorite=1, statut='Réalisée', date_id=3, projet_id=1),
        Taches(id_tache=2, libelle='Tache B', description='Tester le module de connexion', niveau_profondeur=2, duree=8, avancement=50.00, priorite=2, statut='En cours', date_id=1, projet_id=2),
        Taches(id_tache=3, libelle='Tache C', description='Développer la fonctionnalité principale', niveau_profondeur=1, duree=10, avancement=30.00, priorite=3, statut='Planifiée', date_id=1, projet_id=3),
    ]
    Taches.objects.bulk_create(taches)

if __name__ == '__main__':
    # Appelez la fonction pour créer et insérer les données fictives
    create_initial_data()
