from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/home.html')


def match_new(request):

    return render(request, 'core/match_new.html')


def store_choice(request):
    return render(request, 'core/store_choice.html')