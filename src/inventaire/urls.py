from django.urls import path
from . import views

urlpatterns = [
    #homepage
    path('', views.home, name="homepage"),

    path('/connect', views.home, name="connexion"), #Need an update
    path('/disconnect', views.home, name="deconnexion") #Need an update
]
