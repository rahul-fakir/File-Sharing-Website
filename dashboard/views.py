from django.shortcuts import render
from catalog.models import Categories

def main(request):
    categories = Categories.objects.all()
    return render(request, "dashboard.html", {'categories': categories})