import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    univ = profile.univ

    if request.method == "POST":
        menu_name = request.POST['menu_name']
        print(menu_name)
        menu_price = request.POST['menu_price']
        with_num = request.POST['with_num']
        posting_time = request.POST['posting_time']
        # on_store = Store.objects.get(title='store_title').id
        # cat_name = request.POST['cat_name']
        # store_filter = Store.objects.filter(cat_name=cat_name)
        # store_title = request.POST['store_name']
        pk = request.POST['store_pk']
        store_id = Store.objects.get(pk=pk)
        print(1)
        on_posting = Posting.objects.create(
            user_id=current_user,
            store_id=store_id,
            menu=menu_name,
            price=menu_price,
            max_num=with_num,
            timer=posting_time,
            finished=False
        )
        print(2)
        on_posting.save()
        return render(request, 'core/match_fin.html', {'profile': profile, 'univ': univ})
    else:
        data = {
            # 'store': store,
            'profile': profile,
            'univ': univ
        }
        return render(request, 'core/match_new.html', data)


def choice_detail(request):
    cat_list = ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점']
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    stores_univ = Store.objects.filter(univ_id=profile.univ)
    stores = Store.objects.all()
    # store_치킨 = Store.objects.filter(cat_name='치킨')

    if request.method == 'POST':
        stores = Store.objects.all()
        store_title = request.POST.get('title')

        data = {
            'profile': profile,
            'cat_list': cat_list,
            'stores': stores,
            'stores_univ': stores_univ,
            'store_title': store_title,
        }
        return render(request, 'core/match_new.html', data)
    else:
        # paginator = Paginator(stores_univ, 20)
        # page = request.GET.get('page', 1)
        # stores_in_page = paginator.get_page(page)
        # try:
        #     lines = paginator.page(page)
        # except PageNotAnInteger:
        #     lines = paginator.page(1)
        # except EmptyPage:
        #     lines = paginator.page(paginator.num_pages)
        data = {
            'profile': profile,
            'cat_list': cat_list,
            'stores': stores,
            # 'stores_univ': lines,
            # 'stores_in_page': stores_in_page,
        }
        return render(request, 'core/choice_detail.html', data)


def match_fin(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    univ = profile.univ
    data = {
        # 'store': store,
        'profile': profile,
        'univ': univ
    }
    return render(request, 'core/match_fin.html', data)


def mypage(request):
    return render(request, 'core/mypage.html')



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


def allProdCat(request, c_slug=None):
    c_page = None
    store_list = None
    if c_slug != None:
        c_page = get_object_or_404(Store, slug=c_slug)
        store_list = Store.objects.filter(cat_name=c_page, available=True)
    else:
        store_list = Store.objects.all().filter(available=True)

    paginator = Paginator(store_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        stores = paginator.page(page)
    except(EmptyPage, InvalidPage):
        stores = paginator.page(paginator.num_pages)

    return render(request, 'core/choice_detail.html', {'category':c_page, 'stores':stores})