from django.db import models
from django.contrib.auth.models import AbstractUser

"""
Classe définissant les utilisateurs du système
"""
class CustomUser(AbstractUser):
    #Identifiant de la carte d'accès du lycée'
    cardid = models.CharField(blank=True, max_length=50, unique=True)

    #Numéro de téléphone
    phone = models.CharField(blank=True, max_length=20)

    #Type d'utilisateur (cf. liste)
    usertype = models.IntegerChoices("Type d'utilisateur", "Élève Enseignant Administratif")
    STUDENT = 1
    TEACHER = 2
    ADMINISTRATOR = 3

    #Genre
    gender = models.IntegerChoices("Genre", "Homme Femme")
    MALE,_ = gender.choices[0]
    FEMALE,_ = gender.choices[1]

    #Sont inclus d'office : Nom, prénom, identifiant, mot de passe, courriel

    USERNAME_FIELD = "cardid"
    REQUIRED_FIELDS = []


""""
Classe définissant les emplacements de stockage. Chaque niveau d'emplacement
doit être défini, par exemple : Bâtiment H, puis Salle H110 Bis, puis
Armoire du fond, puis étage, ..., selon le degré de précision souhaité
"""
class Place(models.Model):
    #Nom de l'emplacement. Par exemple : H110, Armoire n°3, bâtiment J, etc.
    designation = models.CharField(max_length=200)

    #Le type d'emplacement (ou le mode de rangement à l'intérieur)
    placetype = models.IntegerChoices("Type de conteneur", "Unique Ligne Colonne Grille")

    #Le nombre de rangées de stockage
    lines = models.PositiveSmallIntegerField(blank=True)

    #Le nombre de colonnes de stockage
    columns = models.PositiveSmallIntegerField(blank=True)

    #Le nombre de cases de rangement disponible dans un emplacement
    subpositions = models.PositiveSmallIntegerField(blank=True)

    #L'emplacement parent de l'emplacement, s'il existe.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    #Nom court pour générer un code d'emplacement
    referencename = models.CharField(max_length=10)


"""
Classe définissant les fournisseurs des composants stockés.
"""
class Suppliers(models.Model):
    #Nom commercial du fournisseur
    name = models.CharField(unique=True, max_length=200)

    #URL du site web du fabriquant, laisser vide s'il n'y en a pas
    website = models.URLField(blank=True)

    #Courriel du contact commercial
    email = models.EmailField(blank=True)

    #Téléphone du fournisseur
    phone = models.CharField(blank=True, max_length=20)

    #Adresse postale du fournisseur
    adress = models.CharField(blank=True, max_length=254)
    zipcode = models.PositiveIntegerField(blank=True)
    city = models.CharField(blank=True, max_length=150)
    country = models.CharField(blank=True, max_length=150)

    #Délai moyen de livraison du fournisseur
    supplydelay = models.IntegerChoices("Délai de livraison", "Rapide Moyen Lent")


"""
Classe définissant les objets stockés dans l'inventaire. Si un item identique
est stocké à plusieurs endroits, il devra être créé plusieurs fois.
"""
class Item(models.Model):
    #Désignation de l'objet (généralement un nom compréhensible)
    designation = models.CharField(max_length=254)

    #Une description complète du composant et de son intérêt
    description = models.TextField(blank=True)

    #Identifiant scanner de codes barres
    idbarcodescanner = models.CharField(max_length=100)

    #Emplacement de l'élément
    position = models.ForeignKey(Place, on_delete=models.PROTECT)
    positionline = models.PositiveSmallIntegerField(blank=True)
    positioncolumn = models.PositiveSmallIntegerField(blank=True)
    positionsubposition = models.PositiveSmallIntegerField(blank=True)

    #Nombre de composants en stock
    quantity = models.PositiveIntegerField()

    #Le composant est-il un consommable ou un composant réutilisable
    #Les composants consommables sont définitivement sortis du stock en cas d'emprunt
    consumable = models.BooleanField()

    #Image du composant
    image = models.ImageField(upload_to="uploads/images/%Y/%m/%d/", max_length=250, blank=True)


"""
Classe permettant de faire le lien entre les items et les derniers tarifs
connus de cet item chez nos principaux fournisseurs.
"""
class ItemSuppliers(models.Model):
    #Item concerné
    itemid = models.ForeignKey(Item, on_delete=models.CASCADE)

    #Fournisseur concerné
    supplierid = models.ForeignKey(Suppliers, on_delete=models.CASCADE)

    #Dernier prix connu
    lastprice = models.DecimalField(max_digits=20, decimal_places=3)
    taxes = models.IntegerChoices("Taxes", "HT TTC")

    #Référence fournisseur
    supplierreference = models.CharField(max_length=254)


"""
Classe listant les ressources disponibles pour chaque item
"""
class ItemRessource(models.Model):
    #Item concerné
    itemid = models.ForeignKey(Item, on_delete=models.CASCADE)

    #Type de ressource
    ressourcetype = models.IntegerChoices("Type de ressource", "Driver Documentation Exemple Sources")

    #Lien vers la ressource
    ressourceurl = models.URLField(blank=True)
    ressourcefile = models.FileField(upload_to="uploads/ressources/%Y/%m/%d/", blank=True, max_length=200)


"""
Classe contenant les caractéristiques techniques des composants stockés
"""
class Characteristics(models.Model):
    #Nom de la caractéristique
    name = models.CharField(max_length=50)

    #Unité de la caractéristique
    unit = models.CharField(max_length=50, blank=True)

    #Valeur de la caractéristique
    value = models.CharField(max_length=254)

    #Item concerné
    itemid = models.ForeignKey(Item, on_delete=models.CASCADE)


"""
Classe listant les emprunts effectués
"""
class Rental(models.Model):
    #Utilisateur concerné
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="userid")

    #Utilisateur gérant l'emprunt
    renterid = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="renterid", blank=True, null=True)

    #Date d'emprunt
    rentdate = models.DateTimeField(auto_now_add=True)

    #Date de retour théorique
    returndate = models.DateTimeField()

    #Date de clôture de l'emprunt (tout est soldé)
    closedate = models.DateTimeField()

    #Type de clôture
    CLOTURE_CHOICES = {
    "ATTENTE": "Clôture non effectuée",
    "COMPLET": "Retour complet",
    "FACTURE": "Matériel Facturé (perte ou casse volontaire)",
    "CASSE": "Matériel cassé (dans un cadre pédagogique)",
    "PROJET": "Implanté dans un projet",
    }
    closestatus = models.CharField(choices=CLOTURE_CHOICES, default="ATTENTE", max_length=10)

    #Commentaire sur l'emprunt
    comment = models.TextField(blank=True)


"""
Classe recensant tous les éléments empruntés
"""
class RentalItem(models.Model):
    #Emprunt concerné
    rentalid = models.ForeignKey(Rental, on_delete=models.CASCADE)

    #Item concerné
    itemid = models.ForeignKey(Item, on_delete=models.CASCADE)

    #Quantité empruntée
    quantity = models.PositiveIntegerField()

    #Date de retour du composant
    returndate = models.DateTimeField(blank=True)

    #Quantité retournée
    returnedquantity = models.PositiveIntegerField(blank=True)

    #Quantitée perdue, cassée ou volée
    lostquantity = models.PositiveIntegerField(blank=True)
