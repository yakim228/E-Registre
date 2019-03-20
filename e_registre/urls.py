"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'e_registre'

urlpatterns = [
    path(r'login/',views.login_page,name="login"),
    path(r'logout/',views.logout_page,name="logout"),
    path(r'add/<personnes>',views.index,name="index"),
    path(r'personne.<personne_id>/',views.personne_detail,name="personne_detail"),
    path(r'personnes/<personnes>',views.personnes,name="liste_personnes"),
    path(r'home/',views.home,name="home"),
    path(r'visites/',views.visites,name="visites"),
    path(r'recherche/',views.search,name="search"),
    path(r'motif/',views.motif,name="motif"),
    path(r'register/',views.s_enregistrer,name="register"),
]
