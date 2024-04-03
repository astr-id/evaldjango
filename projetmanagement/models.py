from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, Group, AbstractUser
from datetime import datetime, date
from django.utils import timezone


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
    STATUT_CHOICES = (
        ('Arrêt maladie', 'Arrêt maladie'),
        ('Congés', 'Congés'),
    )
    type = models.CharField(max_length=50, choices=STATUT_CHOICES)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)


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
            statut__in=['Validée']).count() == self.taches_set.count()
        toutes_taches_pauses = self.taches_set.filter(
            statut__in=['En pause']).count() == self.taches_set.count()
        toutes_taches_realisees = self.taches_set.filter(
            statut__in=['Réalisée']).count() == self.taches_set.count()
        if toutes_taches_terminees:
            self.statut = 'Livré'
            self.save()
            return
        if toutes_taches_pauses:
            self.statut = 'En pause'
            self.save()
            return
        if toutes_taches_realisees:
            self.statut = "En cours"
            self.save()
            return
        # Si une des taches est en cours, alors le projet est en cours.
        for tache in self.taches_set.all():
            if tache.statut == 'En cours':
                self.statut = 'En cours'
                self.save()
                return
        # Si une des taches est en planifiée, alors le projet est planifié
        for tache in self.taches_set.all():
            if tache.statut == 'Planifiée':
                self.statut = 'Planifié'
                self.save()
                return


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
    employes = models.ManyToManyField(Utilisateur, related_name='taches_assignees', blank=True)
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
        self.calculer_avancement()
        self.mettre_a_jour_statut_parent()

    def __str__(self):
        return self.libelle

    def calculer_avancement(self):
        if self.sous_taches.exists():
            avancements = [sous_tache.avancement for sous_tache in self.sous_taches.all()]
            avancement_moyen = sum(avancements) / len(avancements)
            self.avancement = avancement_moyen
        else:
            self.avancement = 0

        if self.tache_parent:
            self.tache_parent.calculer_avancement()

    def mettre_a_jour_statut_parent(self):
        if self.tache_parent:
            statuts_sous_taches = set(sous_tache.statut for sous_tache in self.tache_parent.sous_taches.all())

            if 'En cours' in statuts_sous_taches:
                self.tache_parent.statut = 'En cours'
            elif 'Réalisée' in statuts_sous_taches and len(statuts_sous_taches) == 1:
                self.tache_parent.statut = 'Réalisée'
            elif 'Validée' in statuts_sous_taches and len(statuts_sous_taches) == 1:
                self.tache_parent.statut = 'Validée'
            self.tache_parent.save()

            if self.tache_parent and self.tache_parent.statut == 'En pause':
                self.mettre_a_jour_statut_enfant()

    def mettre_a_jour_statut_enfant(self):
        for sous_tache in self.sous_taches.all():
            sous_tache.statut = 'En pause'
            sous_tache.save()

    def mettre_a_jour_statut_absence(self):
        employes_tache = self.employes.all()
        employes_absents = []
        debut_tache = self.date_debut
        fin_tache = self.date_fin
        aujourdhui = timezone.now().date()

        for employe in employes_tache:
            dates_absence = Dates.objects.filter(utilisateur=employe.id)
            for date in dates_absence:
                if date.debut < aujourdhui and date.fin > aujourdhui:
                    employes_absents.append(employe)

        if len(employes_absents) == len(employes_tache):
            self.statut = "En pause"
        else:
            self.statut = self.statut

        self.save()

    #  Check s'il n'y a plus d'employes et que la tache est en cours, la mettre en pause
    def check_employe(self):
        print(self.employes)
        if not self.employes.exists() and self.statut == 'En cours':
            self.statut = 'En pause'
            return True
        return False

    def mettre_a_jour_statut_absence(self):
        employes_tache = self.employes.all()
        employes_absents = []
        aujourdhui = timezone.now().date()

        for employe in employes_tache:
            dates_absence = Dates.objects.filter(utilisateur=employe.id)
            for date in dates_absence:
                if date.debut < aujourdhui and date.fin > aujourdhui:
                    employes_absents.append(employe)

        if len(employes_absents) == len(employes_tache):
            self.statut = "En pause"
        else:
            self.statut = self.statut

        self.save()
