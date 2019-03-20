from .models import Visite
 
 
def recent_visites(request):
    return dict(recent_visites=Visite.objects.all().order_by("-heure_darrivee")[:8])