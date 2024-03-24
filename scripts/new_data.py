import os
import django

# Configurez les paramètres de l'application Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaldjango.settings')
django.setup()

# Importez les modèles
from projetmanagement.models import Utilisateur, Dates, Projets, Taches

def create_additional_data():
    # Créez des instances supplémentaires pour chaque modèle avec des données fictives
    utilisateurs = [
        Utilisateur(id_utilisateur=4, nom='Lefevre', role='Gestionnaire', prenom='Sophie'),
        Utilisateur(id_utilisateur=5, nom='Moreau', role='Employé', prenom='Luc'),
        Utilisateur(id_utilisateur=6, nom='Roux', role='Responsable', prenom='Anne'),
    ]
    Utilisateur.objects.bulk_create(utilisateurs)

    dates = [
        Dates(id_date=4, debut='2024-06-01', fin='2024-06-15', type='Congés'),
        Dates(id_date=5, debut='2024-07-01', fin='2024-07-30', type='Formation'),
        Dates(id_date=6, debut='2024-08-01', fin='2024-08-10', type='Projet'),
    ]
    Dates.objects.bulk_create(dates)

    projets = [
        Projets(id_projet=4, nom='Projet D', avancement=30.00, statut='En pause', responsable_id=4, date_id=4),
        Projets(id_projet=5, nom='Projet E', avancement=90.00, statut='Planifié', responsable_id=5, date_id=5),
        Projets(id_projet=6, nom='Projet F', avancement=60.00, statut='En cours', responsable_id=6, date_id=6),
    ]
    Projets.objects.bulk_create(projets)

    taches = [
        Taches(id_tache=4, libelle='Tache D', description='Tester le nouveau module', niveau_profondeur=1, duree=7, avancement=40.00, priorite=2, statut='En cours', date_id=6, projet_id=6),
        Taches(id_tache=5, libelle='Tache E', description='Débugger les erreurs', niveau_profondeur=2, duree=5, avancement=20.00, priorite=3, statut='Planifiée', date_id=4, projet_id=4),
        Taches(id_tache=6, libelle='Tache F', description='Implémenter la nouvelle fonctionnalité', niveau_profondeur=1, duree=10, avancement=50.00, priorite=1, statut='En cours', date_id=5, projet_id=5),
    ]
    Taches.objects.bulk_create(taches)

if __name__ == '__main__':
    # Appelez la fonction pour créer et insérer les données fictives supplémentaires
    create_additional_data()
