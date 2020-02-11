from django.contrib.auth.models import User
from django.shortcuts import render
from core.models import Category, Store
from account.models import Univ, Profile


def home(request):
    return render(request, 'core/home.html')


def match_new(request, pk):
    univ = request.user.profile.univ
    univ_input = Profile.objects.filter(name=univ)
    categories = Category.objects.get()
    stores = Store.objects.all()
    return render(request, 'core/match_new.html')


def choice_page(request):
    return render(request, 'core/store_choice.html')


def match_fin(request):
    return render(request, 'core/match_fin.html')

