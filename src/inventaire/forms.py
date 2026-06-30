from django import forms
from .models import *

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        widgets = {
            'image': forms.FileInput(),
            'consumable':forms.CheckboxInput(),
            'pk':forms.HiddenInput(),

        }
        labels = {
            "designation": "Désignation",
            "description": "Description",
            "idbarcodescanner": "Code d'identification produit",
            "quantity": "Quantité",
            "consumable": "Le produit est un consommable",
            "image": "Image du produit",
            "positionline":"Ligne",
            "positioncolumn":"Colonne",
            "positionsubposition":"Emplacement"
        }

class CharacteristicsForm(forms.ModelForm):
    class Meta:
        model = Characteristics
        fields = "__all__"
        widgets = {
            'itemid':forms.HiddenInput(),
            'pk':forms.HiddenInput(),
        }
        labels = {
            "name": "Nom",
            "unit": "Unité",
            "value": "Valeur",
        }


class RessourcesForm(forms.ModelForm):
    class Meta:
        model = ItemRessource
        fields = "__all__"
        widgets = {
            'itemid':forms.HiddenInput(attrs={'id': 'res_itemid'}),
            'pk':forms.HiddenInput(attrs={'id': 'res_pk'}),
            'ressourcefile':forms.FileInput
        }
        labels = {
            "ressourcename": "Nom de la ressource",
            "ressourcetype": "Type de ressource",
            "ressourceurl": "URL de la ressource (si absence de fichier)",
            "ressourcefile": "Fichier"
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = "__all__"
        widgets = {
            'pk':forms.HiddenInput(attrs={'id': 'sup_pk'}),
        }
        labels = {
            "name": "Nom",
            "website": "Site Web",
            "email": "Courriel",
            "phone": "N° de téléphone",
            "address": "Adresse",
            "zipcode": "CP",
            "city": "Ville",
            "country": "Pays",
            "supplydelay": "Délai moyen de livraison"
        }
