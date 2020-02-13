from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

<<<<<<< Updated upstream
from django.forms import forms
from django.shortcuts import render
from core.models import Store, Posting
from account.models import Univ, Profile


def home(request, pk):
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)
    univ = profile.univ
    # categories = Category.objects.filter(univ_id=univ)
    postings = Posting.objects.filter(user_id=current_user.id)
    data = {
        'postings': postings,
=======
    categories = Category.objects.filter(univ_name=univ)
    data = {
>>>>>>> Stashed changes
        'postings': postings,
        'current_user': current_user.id,
        'univ': univ,
        'profile': profile,
        #'categories': categories,
    }
    return render(request, 'core/home.html', data)



def match_new(request, pk):
    univ = request.user.profile.univ
    univ_input = Profile.objects.filter(name=univ)
    # categories = Category.objects.get()
    stores = Store.objects.all()
    if request.method == "POST":
        pass
    else:
        pass
    return render(request, 'core/match_new.html')


<<<<<<< Updated upstream
def choice_cat(request, pk):
    # cats = Category.objects.all()
    if request.method == 'POST':
        pass
    else:
        data = {
           # 'cats':cats,
        }
    return render(request, 'core/choice_cat.html', data)


def choice_store(request):
    return render(request, 'core/choice_store.html')
=======
<<<<<<< HEAD
def choice_page(request):
    return render(request, 'core/store_choice.html')
>>>>>>> Stashed changes


def match_fin(request):
    return render(request, 'core/match_fin.html')


def mypage(request):
    return render(request, 'core/mypage.html')
<<<<<<< Updated upstream
=======
=======
def store_choice(request):
    return render(request, 'core/store_choice.html')
>>>>>>> Stashed changes

def main(request):
    univs = Univ.objects.all()
    data = {
        'univs': univs
    }
    return render(request, 'core/main.html', data)
<<<<<<< Updated upstream


# class UploadFileForm(forms.Form):
#     file = forms.FileField()
#
#
# # Create your views here.
# def upload(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             filehandle = request.FILES['file']
#             return excel.make_response(filehandle.get_sheet(), "xlsx",
#                                        file_name="download")
#     else:
#         form = UploadFileForm()
#     return render(
#         request,
#         'upload_form.html',
#         {
#             'form': form,
#             'title': 'Excel file upload and download example',
#             'header': ('Please choose any excel file ' +
#                        'from your cloned repository:')
#         })
=======
>>>>>>> KSH_POSTING
>>>>>>> Stashed changes
