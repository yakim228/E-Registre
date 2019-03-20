from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Etudiant)
admin.site.register(Visiteur)
admin.site.register(Visite)
admin.site.register(Personne)
admin.site.register(Personnel)