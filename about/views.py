#coding: utf8
from django.shortcuts import render
from catalog.models import Categories



def main(request):
    categories = Categories.objects.all()
    return render(request, "about.html", {'categories': categories})