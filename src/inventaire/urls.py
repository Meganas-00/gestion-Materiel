from django.urls import path
from . import views, viewssuppliers

urlpatterns = [
    #homepage
    path('', views.home, name="homepage"),
    path('composants/', views.components, name="components"),
    path('composants/list/<int:page>/', views.components, name="components"),

    # Barre de recherche
    path('composants/search/', views.componentssearch, name="componentssearch"),
    path('composants/search/<str:search>/', views.componentssearch, name="componentssearch"),
    path('composants/search/<str:search>/<int:page>/', views.componentssearch, name="componentssearch"),

    #Configuration des items
    path('item/new/', views.itemproperty, name="itemproperty"),
    path('item/<int:id>/', views.itemproperty, name="itemproperty"),
    path('item/add/', views.itemsave, name="itemadd"),
    path('item/update/<int:id>', views.itemsave, name="itemupdate"),
    path('item/remove/<int:id>', views.itemdelete, name="itemdelete"),

    #Caractéristiques des items
    path('item/<int:id>/caracteristiques', views.itemcharacteristics, name="itemcaract"),
    path('item/<int:id>/caracteristiques/form/', views.itemcharacteristicsform, name="itemcaractform"),
    path('item/<int:id>/caracteristiques/form/<int:caractid>', views.itemcharacteristicsform, name="itemcaractform"),
    path('item/<int:id>/caracteristiques/add/', views.itemcharacteristicsadd, name="itemcharactadd"),
    path('item/<int:id>/caracteristiques/update/<int:caractid>', views.itemcharacteristicsadd, name="itemcharactadd"),
    path('item/<int:id>/caracteristiques/delete/<int:caractid>', views.itemcharacteristicsdelete, name="itemproperty"),

    #Ressources des items
    path('item/<int:id>/ressources', views.itemressources, name="itemcaract"),
    path('item/<int:id>/ressources/form/', views.itemressourcesform, name="itemcaractform"),
    path('item/<int:id>/ressources/form/<int:caractid>', views.itemressourcesform, name="itemcaractform"),
    path('item/<int:id>/ressources/add/', views.itemressourcesadd, name="itemcharactadd"),
    path('item/<int:id>/ressources/update/<int:caractid>', views.itemressourcesadd, name="itemcharactadd"),
    path('item/<int:id>/ressources/delete/<int:caractid>', views.itemressourcesdelete, name="itemproperty"),

    #Fournisseurs
    path('fournisseurs/', viewssuppliers.suppliers, name="suppliers"),
    path('fournisseurs/list/<int:page>/', viewssuppliers.suppliers, name="suppliers"),
    path('fournisseur/new/', viewssuppliers.supplier, name="supplierproperty"),
    path('fournisseur/<int:id>/', viewssuppliers.supplier, name="supplierproperty"),
    path('fournisseur/add/', viewssuppliers.suppliersave, name="suplierupdate"),
    path('fournisseur/update/<int:id>', viewssuppliers.suppliersave, name="supplierupdate"),
    path('fournisseur/remove/<int:id>', viewssuppliers.supplierdelete, name="supplierdelete"),

    # Barre de recherche
    path('fournisseurs/search/', viewssuppliers.supplierssearch, name="supplierssearch"),
    path('fournisseurs/search/<str:search>/', viewssuppliers.supplierssearch, name="supplierssearch"),
    path('fournisseurs/search/<str:search>/<int:page>/', viewssuppliers.supplierssearch, name="supplierssearch"),

    #Tarifs fournisseurs
    path('item/<int:id>/prix', views.itemprice, name="itemprix"),
    path('item/<int:id>/prix/form/', views.itempriceform, name="itemprixform"),
    path('item/<int:id>/prix/form/<int:priceid>', views.itempriceform, name="itemprixform"),
    path('item/<int:id>/prix/add/', views.itempriceadd, name="itemprixadd"),
    path('item/<int:id>/prix/update/<int:priceid>', views.itempriceadd, name="itemprixadd"),
    path('item/<int:id>/prix/delete/<int:priceid>', views.itempricedelete, name="itemprixdelete"),


    # Authentification
    path('connect', views.home, name="connexion"), #Need an update
    path('disconnect', views.home, name="deconnexion"), #Need an update
]
