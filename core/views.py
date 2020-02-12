from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from core.models import Category, Store
from account.models import Univ, Profile


def home(request, pk):
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)
    univ = profile.univ
    categories = Category.objects.filter(univ_name=univ)
    data = {
        'current_user': current_user.id,
        'univ': univ,
        'profile': profile,
        'categories': categories,
    }
    return render(request, 'core/home.html', data)



def match_new(request, pk):
    univ = request.user.profile.univ
    locations = Univ.objects.filter(name=univ)
    categories = Category.objects.get()
    stores = Store.objects.all()
    return render(request, 'core/match_new.html')


def store_choice(request):
    return render(request, 'core/store_choice.html')

def main(request):
    univs = Univ.objects.all()
    data = {
        'univs': univs
    }
    return render(request, 'core/main.html', data)