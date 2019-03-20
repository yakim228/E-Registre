from django.db import models
import datetime
from django.conf import settings
# Create your models here.

class Personne(models.Model):
	nom = models.CharField(max_length=30)
	prenom = models.CharField(max_length=35)
	sexe = models.CharField(max_length=10)
	telephone = models.CharField(max_length=13)	

	def __str__(self):
		return "Personne: "+self.nom


class Visiteur(Personne):
	def __str__(self):
		return "Visiteur: "+self.nom

class Etudiant(Personne):
	def __str__(self):
		return "Etudiant: "+self.nom
class Personnel(Personne):
	def __str__(self):
		return "Personnel: "+self.nom
User = settings.AUTH_USER_MODEL
class Visite(models.Model):
	personne = models.ForeignKey('Personne',on_delete=models.CASCADE,default=None,null=True)
	date_de_visite = models.DateField(null=True)
	heure_darrivee = models.DateTimeField(null=True)
	heure_depart = models.DateTimeField(null=True)
	motif = models.TextField(null=True)

	def __str__(self):
		return "Visite: "+self.personne.nom







