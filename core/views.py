import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.forms import forms
from django.shortcuts import render
from core.models import Store, Posting, Tag

from chat.models import Room, Contact
from core.models import Store
from account.models import Univ, Profile


def home(request, pk):
    if request.user.is_authenticated:
        current_user = request.user
        profile = Profile.objects.get(user=current_user)
        univ = profile.univ
        stores = Store.objects.filter(univ_id=pk)
        postings = []
        for store in stores:
            postings += Posting.objects.filter(store_id=store.id)
        tags = []
        for posting in postings:
            tags += Tag.objects.filter(posting_id=posting)
        data = {
            'postings': postings,
            'current_user': current_user.id,
            'univ': univ,
            'profile': profile,
            'categories': ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점'],
            'tags': tags
        }
        return render(request, 'core/home.html', data)
    else:
        stores = Store.objects.filter(univ_id=pk)
        univ = Univ.objects.get(pk=pk)
        univs = Univ.objects.all()
        postings = []
        for store in stores:
            postings2 = Posting.objects.filter(store_id=store.id)
            for posting in postings2:
                postings.append(posting)
        tags=[]
        for posting in postings:
            tags += Tag.objects.filter(posting_id=posting.id)
        data = {
            'postings': postings,
            'univ': univ,
            'univs': univs,
            'categories': ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점'],
            'tags': tags
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


def choice_page(request):
    return render(request, 'core/store_choice.html')


def match_fin(request):
    return render(request, 'core/match_fin.html')


def mypage(request):
    return render(request, 'core/mypage.html')


def store_choice(request):
    return render(request, 'core/store_choice.html')


def main(request):
    if request.user.is_authenticated:
        current_user = request.user
        profile = Profile.objects.get(user=current_user)
        data = {
            'profile': profile
        }
    else:
        univs = Univ.objects.all()
        data = {
            'univs': univs
        }
    return render(request, 'core/main.html', data)


def search(request):
    return render(request, 'core/search.html')


def search_store(request):
    kwd = request.POST.get('kwd', None)
    data = {
        'content': list()
    }
    if kwd:
        postings = Posting.objects.filter(menu__icontains=kwd)
        for posting in postings:
            data['content'].append({
                'menu': posting.menu,
                'price': posting.price,
                'max_num': posting.max_num
            })
    return HttpResponse(json.dumps(data), content_type="application/json")

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
