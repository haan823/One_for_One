import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.forms import forms
from django.shortcuts import render
from core.models import Store, Posting

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
        data = {
            'postings': postings,
            'current_user': current_user.id,
            'univ': univ,
            'profile': profile,
            'categories': ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점'],
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
        data = {
            'postings': postings,
            'univ': univ,
            'univs': univs,
            'categories': ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점'],
        }
        return render(request, 'core/home.html', data)

def match_new(request):
    # univ = request.user.profile.univ
    # # stores = Store.objects.filter(name=univ)
    # if request.method == "POST":
    #     return render(request, 'core/match_fin.html')
    # else:
    #     pass
    return render(request, 'core/match_new.html')


<<<<<<< HEAD
def choice_cat(request, pk):
    # cats = Category.objects.all()
    if request.method == 'POST':
        pass
    else:
        data = {
            # 'cats':cats,
        }
=======
def choice_cat(request):
    cat_list = ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점']
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    stores_univ = Store.objects.filter(univ_id=profile.univ)
    stores = Store.objects.all()
    data = {
        'cat_list': cat_list,
        'stores': stores,
    }
>>>>>>> KBH_crawling
    return render(request, 'core/choice_cat.html', data)


def choice_detail(request):
    cat_list = ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점']
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    stores_univ = Store.objects.filter(univ_id=profile.univ)

    data = {
        'cat_list': cat_list,
        'stores_univ': stores_univ
    }
    return render(request, 'core/choice_detail.html')


def choice_page(request):
    return render(request, 'core/store_choice.html')


def match_fin(request):
    return render(request, 'core/match_fin.html')


def mypage(request):
    return render(request, 'core/mypage.html')


<<<<<<< HEAD
def store_choice(request):
    return render(request, 'core/store_choice.html')


=======
>>>>>>> KBH_crawling
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
<<<<<<< HEAD
=======

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
    cat_list = ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점']
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    stores_univ = Store.objects.filter(univ_id=profile.univ)
    stores = Store.objects.all()
    data = {
        'cat_list': cat_list,
        'stores': stores,
    }
    return render(request, 'core/test.html', data)


def test_choice(request):
    if request.method == 'POST':
        cat = request.POST['cat']
        return redirect(reverse('core:test_choice', args=[cat]))
    else:
        cat_list = ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점']
        img_list = ['치킨.jpg', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점']
        data = {
            'cat_list': cat_list,
        }
        return render(request, 'core/test_choice.html', data)


def new_test(request):
    cat_list = ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점']
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    stores_univ = Store.objects.filter(univ_id=profile.univ)
    stores = Store.objects.all()
    data = {
        'cat_list': cat_list,
        'stores': stores,
        'stores_univ': stores_univ,
    }
    return render(request, 'core/new_test.html', data)
>>>>>>> KBH_crawling
