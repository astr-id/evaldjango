from django.db import models


class Utilisateur(models.Model):
    id_utilisateur = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=50)
    ROLE_CHOICES = (
        ('Employé', 'Employé'),
        ('Responsable', 'Responsable'),
        ('Gestionnaire', 'Gestionnaire'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    prenom = models.CharField(max_length=50)


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
    date = models.ForeignKey(Dates, on_delete=models.SET_NULL, null=True)


class Taches(models.Model):
    id_tache = models.IntegerField(primary_key=True)
    libelle = models.CharField(max_length=255)
    description = models.TextField()
    niveau_profondeur = models.SmallIntegerField()
    duree = models.IntegerField()
    avancement = models.DecimalField(max_digits=15, decimal_places=2)
    PRIORITE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )
    priorite = models.IntegerField(choices=PRIORITE_CHOICES)
    STATUT_CHOICES = (
        ('Planifiée', 'Planifiée'),
        ('En cours', 'En cours'),
        ('Réalisée', 'Réalisée'),
        ('En pause', 'En pause'),
        ('Validée', 'Validée'),
    )
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES)
    tache_parent = models.ForeignKey('self', null=True, blank=True, related_name='sous_taches',
                                     on_delete=models.CASCADE)
    date = models.ForeignKey(Dates, on_delete=models.SET_NULL, null=True)
    projet = models.ForeignKey(Projets, on_delete=models.CASCADE)
