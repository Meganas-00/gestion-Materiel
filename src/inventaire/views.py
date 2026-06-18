from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.conf import settings

def home(request):
    template = loader.get_template("inventaire/base.html")
    return HttpResponse(template.render({}, request))
