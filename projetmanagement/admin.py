from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Projets)
admin.site.register(Taches)
admin.site.register(Utilisateur)
admin.site.register(Dates)