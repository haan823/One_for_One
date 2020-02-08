from django.shortcuts import render
from core.models import Category, Store, Location


def home(request):
    return render(request, 'core/home.html')


def match_new(request):
    locations = Location.objects.get()
    categories = Category.objects.get()
    stores = Store.objects.all()

    return render(request, 'core/match_new.html')


def store_choice(request):
    return render(request, 'core/store_choice.html')