from django import forms
from django.core.exceptions import ValidationError
from .models import Personne, Visiteur, Etudiant,Personnel,Visite
from .utils import Preference, get_current_user
from django.contrib.auth import get_user_model

User = get_user_model()
 
class PersonneForm(forms.ModelForm):
    
    class Meta:
        model = Personne
        fields = ('nom', 'prenom', 'sexe', 'telephone')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'rows': '10',
                                                        'spellcheck': 'false'}),
            'prenom': forms.TextInput(attrs={'class': 'selectpicker foo form-control',
                                            'data-live-search': 'true',
                                            'data-size': '5'}),
            'sexe': forms.Select(attrs={'class': 'selectpicker form-control'},choices=(('1','Homme'),('2','Femme'))),
            'telephone': forms.TextInput(attrs={'class': 'selectpicker form-control','placeholder': '(00228) xx xx xx xx'}),
        }
 
    def save(self, request):
        # get the Snippet object, without saving it into the database
        personne = super(PersonneForm, self).save(commit=False)
        personne.user = get_current_user(request)
        personne.save()    
        return personne
class EtudiantForm(PersonneForm):
    class Meta:
        model = Etudiant
        fields = ('nom', 'prenom', 'sexe', 'telephone')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'rows': '10',
                                                        'spellcheck': 'false'}),
            'prenom': forms.TextInput(attrs={'class': 'selectpicker foo form-control',
                                            'data-live-search': 'true',
                                            'data-size': '5'}),
            'sexe': forms.Select(attrs={'class': 'selectpicker form-control'},choices=(('1','Homme'),('2','Femme'))),
            'telephone': forms.TextInput(attrs={'class': 'selectpicker form-control','placeholder': '(00228) xx xx xx xx'}),
        }
class PersonnelForm(PersonneForm):
    class Meta:
        model = Personnel
        fields = ('nom', 'prenom', 'sexe', 'telephone')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'rows': '10',
                                                        'spellcheck': 'false'}),
            'prenom': forms.TextInput(attrs={'class': 'selectpicker foo form-control',
                                            'data-live-search': 'true',
                                            'data-size': '5'}),
            'sexe': forms.Select(attrs={'class': 'selectpicker form-control'},choices=(('1','Homme'),('2','Femme'))),
            'telephone': forms.TextInput(attrs={'class': 'selectpicker form-control','placeholder': '(00228) xx xx xx xx'}),
        }
class VisiteurForm(PersonneForm):
    class Meta:
        model = Visiteur
        fields = ('nom', 'prenom', 'sexe', 'telephone')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'rows': '10',
                                                        'spellcheck': 'false'}),
            'prenom': forms.TextInput(attrs={'class': 'selectpicker foo form-control',
                                            'data-live-search': 'true',
                                            'data-size': '5'}),
            'sexe': forms.Select(attrs={'class': 'selectpicker form-control'},choices=(('1','Homme'),('2','Femme'))),
            'telephone': forms.TextInput(attrs={'class': 'selectpicker form-control','placeholder': '(00228) xx xx xx xx'}),
        }
class Visite(forms.ModelForm):
    class Meta:
        model = Visite
        fields = ('date_de_visite','heure_darrivee','heure_depart','motif')
        widgets = {
            'date_de_visite':forms.DateInput(attrs={'class': 'form-control'}),
            'heure': forms.Select(attrs={'class': 'selectpicker form-control'},choices=(('1','heure_darrivee'),('2','heure_depart'))),
            'motif': forms.Textarea(attrs={'cols': 40, 'rows': 5}),

        }

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':'form control', 'placeholder':'Entre une recherche'}))
    mypersonne = forms.BooleanField(required=False)
    

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    nom = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        q = User.objects.filter(username=username)
        if q.exists():
            raise forms.ValidationError("ce nom d'utilisateur est deja utiliser")
        return username
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password!=password1:
            raise forms.ValidationError("les mots de passe doivent etre les memes")
        return data