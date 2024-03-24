import os
import django

# Configurez les paramètres de l'application Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaldjango.settings')
django.setup()

# Importez les modèles
from projetmanagement.models import Taches

def creer_taches():
    taches = [
        Taches(id_tache=1, libelle='Tache A', description='Réaliser la documentation', niveau_profondeur=1, duree=5, avancement=100.00, priorite=1, statut='Réalisée', date_id=3, projet_id=1),
        Taches(id_tache=2, libelle='Tache B', description='Tester le module de connexion', niveau_profondeur=2, duree=8, avancement=50.00, priorite=2, statut='En cours', date_id=1, projet_id=2),
        Taches(id_tache=3, libelle='Tache C', description='Développer la fonctionnalité principale', niveau_profondeur=1, duree=10, avancement=30.00, priorite=3, statut='Planifiée', date_id=1, projet_id=3),
    ]
    Taches.objects.bulk_create(taches)

if __name__ == "__main__":
    creer_taches()