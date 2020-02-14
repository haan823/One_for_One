from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

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
        'current_user': current_user.id,
        'univ': univ,
        'profile': profile,
        #'categories': categories,
    }
    return render(request, 'core/home.html', data)


def match_new(request):
    univ = request.user.profile.univ
    Stores = Store.objects.filter(name=univ)
    # categories = Category.objects.get()
    stores = Store.objects.all()
    if request.method == "POST":
        pass
    else:
        pass
    return render(request, 'core/match_new.html')


def choice_cat(request, pk):
    Stores = Store.objects.filter(univ_id=pk)

    if request.method == 'POST':
        pass
    else:
        data = {
           # 'cats':cats,
        }
    return render(request, 'core/choice_cat.html', data)


def choice_store(request):
    return render(request, 'core/choice_store.html')


def match_fin(request):
    return render(request, 'core/match_fin.html')


def mypage(request):
    return render(request, 'core/mypage.html')


def main(request):
    univs = Univ.objects.all()
    data = {
        'univs': univs
    }
    return render(request, 'core/main.html', data)


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

def test_cat(request):
    cat_list = ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점']
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    stores_univ = Store.objects.filter(univ_id=profile.univ)

    data = {
        'cat_list': cat_list,
        # 'stores_univ': [store for store in stores_univ],
        'stores_univ': stores_univ
    }
    return render(request, 'core/test_cat.html', data)


def test(request):
    stores = Store.objects.all()
    data = {
        'stores': stores,
    }
    return render(request, 'core/test.html', data)