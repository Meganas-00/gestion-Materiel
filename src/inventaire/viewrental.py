from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.hashers import check_password

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe

from django.conf import settings

from .forms import *
from .models import *
import time
from datetime import datetime

import json

def rental(request, page=1):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    context = {
        "Title":"Emprunter",
        "Username": request.user.first_name + ' ' + request.user.last_name,
        "Grade": "",
    }

    match(request.user.usertype):
        case CustomUser.STUDENT:
            context["Grade"] = "Élève"

        case CustomUser.TEACHER:
            context["Grade"] = "Enseignant"

        case CustomUser.ADMINISTRATIF:
            context["Grade"] = "Administratif"


    if(request.user.usertype == 1):
        pass

    if(request.user.usertype == 2 or request.user.usertype == 3):
        pass


    if(request.user.usertype <= 1 or request.user.usertype >= 4):
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous n'avez pas les droits nécessaires pour accéder à cette ressource.")

    return render(request, "inventaire/rent.html",context)

def rentuserlist(request, search=""):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    result = None
    if CustomUser.objects.filter(cardid=search).exists():
        result = CustomUser.objects.get(cardid=search)
        return JsonResponse({"type":"Unique",
                             "user":getUser(result.pk)
                             })
    else:
        result = CustomUser.objects.order_by("last_name", "first_name").filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search) | Q(email__icontains=search) | Q(cardid__icontains=search))[:5]
        ret = {"type":"Multiple","values":[]}
        for res in result:
            ret["values"].append(getUser(res.pk))
    return JsonResponse(ret)
    
def getUser(userid):
    if CustomUser.objects.filter(pk=userid).exists():
        result = CustomUser.objects.get(pk=userid)
        return {
                "id":result.pk,
                "first_name":result.first_name,
                "last_name":result.last_name,
                "e-mail":result.email,
                "phone":result.phone,
                "cardid":result.cardid,
                "username":result.username,
                "usertype":result.usertype,
                "NTE":Rental.objects.filter(userid=result).count(),
                "NEC":Rental.objects.filter(userid=result).filter(closestatus="ATTENTE").count(),
                "NER":Rental.objects.filter(userid=result).filter(closestatus="ATTENTE").filter(returndate__lt=datetime.now()).count(),
                "NRD":Rental.objects.filter(userid=result).filter(closestatus="CASSE").count(),
                "NNR":Rental.objects.filter(userid=result).filter(closestatus="FACTURE").count(),
            }
    else:
        return {}



def rentuser(request, userid):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    return JsonResponse(getUser(userid))


def searchcomponent(request, search=""):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    results = Item.objects.order_by("-pk").filter(Q(designation__icontains=search) | Q(description__icontains=search) | Q(idbarcodescanner__icontains=search))
    context = {
        "ListItems": results[:100],
    }

    return render(request, "inventaire/rentcomponentlist.html", context)

def create(request):
    log = request.user.is_authenticated
    if not log:
        return HttpResponseForbidden("Accès à cette ressource non autorisé. Vous devez être connecté pour accéder à cette ressource.")

    utilisateur = get_object_or_404(CustomUser.objects,pk=request.user.pk)

    data = json.loads(request.POST["json"])

    if(check_password(data["validator"]["password"], CustomUser.objects.get(pk=data["validator"]["id"]).password)):
        rent = Rental(userid=CustomUser.objects.get(pk=data["rentUser"]), renterid=CustomUser.objects.get(pk=data["validator"]["id"]),
                    returndate=data["rentDate"], comment=data["rentplace"])
        rent.save()

        for item in data["rentitems"]:
            record = RentalItem(rentalid=rent, itemid=Item.objects.get(pk=item["id"]), quantity=item["quantity"])
            record.save()

    else:
        time.sleep(2)
        return HttpResponse(""" <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                <strong>Mot de passe invalide</strong>
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fermer"></button>
                                </div>""")


    return HttpResponse("Done")

def listrent(request):
    return HttpResponse("Ok")