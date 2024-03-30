from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, Group, AbstractUser


class Utilisateur(AbstractUser):
    estResponsable = models.BooleanField(default=False)
    estGestionnaire = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.estResponsable and self.estGestionnaire:
            raise ValidationError("Une personne ne peut pas être à la fois responsable et gestionnaire.")


class Dates(models.Model):
    id_date = models.IntegerField(primary_key=True)
    debut = models.DateField()
    fin = models.DateField()
    type = models.CharField(max_length=50)


class Projets(models.Model):
    id_projet = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=50)
    avancement = models.DecimalField(max_digits=15, decimal_places=2)
    STATUT_CHOICES = (
        ('En pause', 'En pause'),
        ('Planifié', 'Planifié'),
        ('En cours', 'En cours'),
        ('Livré', 'Livré'),
    )
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES)
    responsable = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def calculer_avancement_moyen(self):
        taches_projet = self.taches_set.all()
        if taches_projet.exists():
            avancements = [tache.avancement for tache in taches_projet]
            avancement_moyen = sum(avancements) / len(avancements)
            self.avancement = avancement_moyen
            self.save()
        else:
            self.avancement = 0
            self.save()

    def verifier_statut_projet(self):
        toutes_taches_terminees = self.taches_set.filter(
            statut__in=['Réalisée', 'Validée']).count() == self.taches_set.count()
        if toutes_taches_terminees:
            self.statut = 'Livré'
            self.save()


# Utile pour vérifier que l'utilisateur gérant la tache a bien l'attribut estGestionnaire à True
def validate_gestionnaire(value):
    if value and not value.estGestionnaire:
        raise ValidationError("L'utilisateur affecté à la tâche doit être un gestionnaire!")


class Taches(models.Model):
    id_tache = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255)
    description = models.TextField()
    niveau_profondeur = models.SmallIntegerField(default=1)
    duree = models.IntegerField()
    avancement = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    PRIORITE_CHOICES = (
        (1, 'Basse'),
        (2, 'Moyenne'),
        (3, 'Haute'),
    )
    priorite = models.IntegerField(choices=PRIORITE_CHOICES, default=2)
    STATUT_CHOICES = (
        ('Planifiée', 'Planifiée'),
        ('En cours', 'En cours'),
        ('Réalisée', 'Réalisée'),
        ('En pause', 'En pause'),
        ('Validée', 'Validée'),
    )
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='Planifiée')
    gestionnaire = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                     validators=[validate_gestionnaire])
    tache_parent = models.ForeignKey('self', null=True, blank=True, related_name='sous_taches',
                                     on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    projet = models.ForeignKey(Projets, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.tache_parent and self.tache_parent.niveau_profondeur >= 3:
            raise ValueError("Impossible d'ajouter une sous-tâche à une tâche de niveau de profondeur supérieur à 2.")
        if self.tache_parent:
            self.niveau_profondeur = self.tache_parent.niveau_profondeur + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle
