
import datetime
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404, reverse,get_list_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.db.models import Q,F
from .models import Personne,Visiteur,Etudiant,Personnel,Visite
from .form import PersonneForm,PersonnelForm,EtudiantForm,VisiteurForm,SearchForm,LoginForm,RegisterForm
from django.utils import timezone
from django.contrib.auth.models import User

from .utils import paginate_result
 
def index(request, personnes):        
    if request.method ==  'POST':
        if personnes=="personnes":
            f = PersonneForm(request.POST)
        if personnes=="personnels":
            f = PersonnelForm(request.POST)
        if personnes=="etudiants":
            f = EtudiantForm(request.POST)
        if personnes=="visiteurs":
            f = VisiteurForm(request.POST)
        if f.is_valid():
            personne = f.save(request)            
            return redirect(reverse('e_registre:personne_detail', args=[personne.id]))
    else:
        if personnes=="personnes":
            f = PersonneForm()
        if personnes=="personnels":
            f = PersonnelForm()
        if personnes=="etudiants":
            f = EtudiantForm()
        if personnes=="visiteurs":
            f = VisiteurForm()
    return render(request, 'e_registre/index.html', {'form': f})

 
def personne_detail(request, personne_id):
    personne = get_object_or_404(Personne, id=personne_id)
    personne.save()
    if 'personne' in request.GET and 'liste' in request.GET:
        personne.delete()
        if request.GET['liste']!='':
            return redirect(reverse('e_registre:liste_personnes',args=[request.GET['liste']]))
        else:
            return redirect(reverse('e_registre:liste_personnes',args=['etudiants']))
        
    visite1 = Visite.objects.filter(personne=personne)
    visites = paginate_result(request, visite1, 5)
    return render(request, 'e_registre/personne_details.html', {'personne': personne,'visites':visites})

def home(request):
    # print(request.session)
    # print(dir(request.session))
    # key = request.session.session_key
    # print(key)
    request.session['first_name'] = "Paul"
    request.session['user'] = request.user.username
    return render(request, 'e_registre/home.html')
    
def visites(request):
    print(request.session.get("first_name","Unknown"))
    visites = Visite.objects.all()
    if 'ordre' in request.GET:
        if request.GET['ordre']=='1':
            visites = visites.order_by('personne__nom')
        if request.GET['ordre']=='2':
            visites = visites.order_by('-personne__nom')
        
        if request.GET['ordre']=='temps1':
            visites = visites.order_by('heure_darrivee')
        if request.GET['ordre']=='temps2':
            visites = visites.order_by('-heure_darrivee')
    if 'query' in request.GET and request.GET['query']!='':
        visites = Visite.objects.filter(personne__nom__icontains = request.GET['query'])
    visites = visites.filter(heure_darrivee__gt=datetime.datetime.today().date())
    visites = paginate_result(request,visites,9)
    return render(request, 'e_registre/visites.html',{'visites':visites})

def logout_page(request):
    logout(request)
    form = LoginForm(request.POST or None)
    print(request.user.is_authenticated)
    context = {'form':form}
    return render(request, 'e_registre/login.html',context)

def personnes(request, personnes):
    liste=""
    if personnes=="personnes":
        liste = Personne.objects.all()
    elif personnes=="visiteurs":
        liste = Visiteur.objects.all()
    elif personnes=="etudiants":
        liste = Etudiant.objects.all()
    elif personnes=="etudiants":
        liste = Etudiant.objects.all()
    else:
        if personnes=="personnels":
            liste = Personnel.objects.all()
    if 'ordre' in request.GET:
        if request.GET['ordre']=='1':
            liste = liste.order_by('nom')
        if request.GET['ordre']=='2':
            liste = liste.order_by('-nom')
    if 'query' in request.GET:
        if request.GET['query']!='':
            liste = liste.filter(Q(nom__icontains=request.GET['query']))
        else:
            liste
    if 'personne1' in request.GET:
        personne1 = Personne.objects.get(id=request.GET['personne1'])
        if 'arrv' in request.GET:
            newVisite = Visite(personne=personne1,heure_darrivee=datetime.datetime.now())
            newVisite.save()
        if 'depa' in request.GET:
            newVisite = Visite.objects.filter(personne=personne1).latest('heure_darrivee')
            if newVisite.heure_depart == None:
                newVisite.heure_depart=datetime.datetime.now()
                newVisite.save()
        return redirect(reverse('e_registre:visites'))

    liste = paginate_result(request, liste, 5)
    return render(request,'e_registre/listes_personnes.html',{'personnes': liste,'pool':personnes,'t':t})

def motif(request):
    personne = None
    if 'id' in request.GET:
        personne = get_object_or_404(Personne,id=request.GET['id'])
    if 'motif' in request.GET:
        visite = Visite.objects.filter(personne=personne).latest('heure_darrivee')
        if visite.motif==None: visite.motif = ''
        visite.motif = str(datetime.datetime.now()) +':'+ request.GET['motif']+visite.motif
        visite.save()
        return redirect(reverse('e_registre:personne_detail',args=[request.GET['id']]))
    return render(request, 'e_registre/motifs.html',{'nom_personne':personne})

def search(request):
    f = SearchForm(request.GET)
    personnes = []
 
    if f.is_valid():
 
        search = f.cleaned_data.get('search')
        
        mypersonnes = f.cleaned_data.get('mypersonne')
 
        # if mypersonne field is selected, search only logged in user's personnes
        if mypersonnes:
            personne_list = Personne.objects.filter(
                Q(nom__icontains=search) | Q(prenom__icontains=search)
            )
 
        else:
            qs1 = Personne.objects.filter(
                Q(prenom__icontains = search) | Q(nom__icontains = search)
                # Q(user=request.user)
            )
            # if the user is logged in then search his personnes
            if request.user.is_authenticated:
               qs2 = Personne.objects.filter(Q(nom__icontains=request.user),
                                            Q(prenom__icontains=search) | Q(nom__icontains=search))
               personne_list = (qs1 | qs2).distinct()
 
            else:
                personne_list = qs1
 
        personnes = paginate_result(request, personne_list, 5)
 
    return render(request, 'e_registre/search.html', {'form': f, 'personnes': personnes })
def visite_detail(request, visite_slug):
    recent_visite = Visite.objects.all().order_by("-heure_darrivee")[:8]
    return render(request, 'e_registre/visite_detail.html', {'recent_visite': recent_visite})
def login_page(request):
    form = LoginForm(request.POST or None)
    print(request.user.is_authenticated)
    context = {'form':form}
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        utilisateur = authenticate(request, username=username,password=password)
        if utilisateur is not None:
            login(request,utilisateur)
            return redirect("/visites")
        else:
            print("erreur")
    
    return render(request,'e_registre/login.html',context)
User = get_user_model()
def s_enregistrer(request):
    rForm = RegisterForm(request.POST or None)
    context = {'rForm':rForm}
    if rForm.is_valid():
        print(rForm.cleaned_data)
        username = rForm.cleaned_data.get('username')
        nom = rForm.cleaned_data.get('nom')
        prenom = rForm.cleaned_data.get('prenom')
        password = rForm.cleaned_data.get('password')
        User.objects.create_user(username=username,password=password,first_name=nom,last_name=prenom)
        return redirect(reverse('e_registre:login'))
    return render(request,'e_registre/signup.html',context)




	



