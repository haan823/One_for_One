import datetime
import json
import math

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.forms import forms
from django.shortcuts import render

from account.utils import send_alarm_sms
from core.models import *

from chat.models import *
from core.models import *
from account.models import *

from core.utils import convert_date_PytoJs


def home(request, pk):

    if request.user.is_authenticated:
        current_user = request.user
        profile = Profile.objects.get(user=current_user.id)
        univ = profile.univ
        contacts = Contact.objects.filter(allowed_user=profile)
        rooms = Room.objects.all()
        stores = Store.objects.filter(univ_id=pk)
        postings = []
        menus = []
        for store in stores:
            postings2 = Posting.objects.filter(store_id=store.id)
            postings3 = postings2
            for posting in postings3:
                postings.append(posting)
        tag_dic = {}
        for posting in postings:
            due = posting.create_date + datetime.timedelta(minutes=posting.timer)
            now = datetime.datetime.now()
            if due > now:
                tags = []
                tags += Tag.objects.filter(posting_id=posting.id)
                posting.create_date_string = convert_date_PytoJs(str(posting.create_date))
                tag_dic[posting] = tags
                menus.append(posting.menu)
        all_tags = set(Tag.objects.all())
        tags_list = []
        for all_tag in all_tags:
            if not all_tag.posting_id.finished:
                tags_list.append(all_tag.content)
        rm_dup_tags = list(set(tags_list))
        data = {
            'contacts': contacts,
            'contacts_num': len(contacts),
            'rooms': rooms,
            'postings': postings,
            'current_user': current_user.id,
            'univ': univ,
            'profile': profile,
            'categories': ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점'],
            'tag_dic': tag_dic,
            'rm_dup_tags': rm_dup_tags,
            'menus': menus,
        }
        return render(request, 'core/home.html', data)
    else:
        stores = Store.objects.filter(univ_id=pk)
        univ = Univ.objects.get(pk=pk)
        univs = Univ.objects.all()
        postings = []
        menus = []
        for store in stores:
            postings2 = Posting.objects.filter(store_id=store.id)
            postings3 = postings2
            for posting in postings3:
                postings.append(posting)
                postings.append(posting)
        tag_dic = {}
        for posting in postings:
            due = posting.create_date + datetime.timedelta(minutes=posting.timer)
            now = datetime.datetime.now()
            if due > now:
                tags = []
                tags += Tag.objects.filter(posting_id=posting.id)
                posting.create_date_string = convert_date_PytoJs(str(posting.create_date))
                tag_dic[posting] = tags
                menus.append(posting.menu)
        all_tags = set(Tag.objects.all())
        tags_list = []
        for all_tag in all_tags:
            if not all_tag.posting_id.finished:
                tags_list.append(all_tag.content)
        rm_dup_tags = list(set(tags_list))
        data = {
            'postings': postings,
            'univ': univ,
            'univs': univs,
            'categories': ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점'],
            'tag_dic': tag_dic,
            'rm_dup_tags': rm_dup_tags,
            'menus': menus
        }
        return render(request, 'core/home.html', data)


def match_new(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    univ = profile.univ
    contacts = Contact.objects.filter(allowed_user=profile)
    if len(contacts) >= 3:
        data = {
            'profile': profile,
            'univ': univ
        }
        return render(request, 'core/not_allowed.html', data)
    elif request.method == "POST":
        menu_name = request.POST['menu_name']
        menu_price = request.POST['menu_price']
        with_num = request.POST['with_num']
        posting_time = request.POST['posting_time']

        store_pk = request.POST['store_pk']
        store_id = Store.objects.get(pk=store_pk)

        menu_change = request.POST['customRadioInline1']
        if menu_change == 'a':
            menu_change = '오늘은 이게 꼭 먹고 싶어요!'
        elif menu_change == 'b':
            menu_change = '다른 메뉴도 좋아요!'
        elif menu_change == 'c':
            menu_change = '상관 없어요!'

        together = request.POST['customRadioInline2']
        if together == 'a':
            together = '같이 먹어요!'
        elif together == 'b':
            together = '따로 먹어요!'
        elif together == 'c':
            together = '상관 없어요!'

        on_posting = Posting.objects.create(
            user_id=current_user,
            store_id=store_id,
            menu=menu_name,
            price=menu_price,
            max_num=with_num,
            timer=posting_time,
            menu_change=menu_change,
            together=together,
        )
        contact = Contact.objects.create(
            posting_id=on_posting,
            allowed_user=Profile.objects.get(user=current_user),
            accepted=True
        )
        contact.save()

        posting_tag1 = request.POST['posting_tag1']
        posting_tag2 = request.POST['posting_tag2']
        posting_tag3 = request.POST['posting_tag3']

        if posting_tag1 is None:
            pass
        else:
            Tag.objects.create(
                posting_id=on_posting,
                content=posting_tag1
            )

        if posting_tag2 is None:
            pass
        else:
            Tag.objects.create(
                posting_id=on_posting,
                content=posting_tag2
            )

        if posting_tag3 is None:
            pass
        else:
            Tag.objects.create(
                posting_id=on_posting,
                content=posting_tag3
            )
        on_posting.save()
        return render(request, 'core/match_fin.html', {'profile': profile, 'univ': univ})
    else:
        data = {
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
        paginator = Paginator(stores_univ, 10)
        page = request.GET.get('page')
        stores_in_page = paginator.get_page(page)

        data = {
            'profile': profile,
            'cat_list': cat_list,
            'stores': stores,
            'stores_univ': stores_univ,
            'stores_in_page': stores_in_page,
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


def my_page(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    contacts = Contact.objects.all()
    user_contacts = contacts.filter(allowed_user=profile)
    expired_postings = []
    now_postings = []
    end_postings = []
    for contact in user_contacts:
        posting_id = contact.posting_id.pk
        posting = Posting.objects.get(pk=posting_id)
        due = posting.create_date + datetime.timedelta(minutes=posting.timer)
        now = datetime.datetime.now()
        if due < now:
            expired_postings.append(posting)
        elif contact.finished == True:
            end_postings.append(posting)
        else:
            now_postings.append(posting)
    context = {
        'rooms': Room.objects.all(),
        'current_user': current_user,
        'profile': profile,
        'now_postings': now_postings,
        'end_postings': end_postings,
        'expired_postings': expired_postings,
        'contacts': contacts,
        'univ': profile.univ_id
    }
    return render(request, 'core/my_page.html', context)


def accept(request, pk):
    contact = Contact.objects.get(pk=pk)
    posting = Posting.objects.get(pk=contact.posting_id.pk)
    if (posting.now_num != posting.max_num):
        posting.now_num += 1
        posting.save()
        contact.accepted = True
        contact.save()
    return redirect('core:my_page')


def refuse(request, pk):
    contact = Contact.objects.get(pk=pk)
    contact.delete()
    phone_number = contact.allowed_user.phone_number
    content = ('<저기요> 상대방이 매칭 신청을 거절했습니다. store: ' + contact.posting_id.store_id.title)
    send_alarm_sms(phone_number, content)

    return redirect('core:my_page')


def delete_posting(request, pk):
    posting = Posting.objects.get(pk=pk)
    messages = Message.objects.filter(room_id=posting.pk)
    messages.delete()
    posting.delete()
    return redirect('core:my_page')


def match_request(request):
    posting_pk = request.GET['posting_pk']
    contacts_num = int(request.GET['contacts_num'])
    posting = Posting.objects.get(pk=posting_pk)
    univ_pk = Profile.objects.get(user=request.user).univ.pk
    contacts = Contact.objects.filter(posting_id=posting)
    if contacts_num > 3:
        print(1)
        raise Exception
    elif posting.now_num == posting.max_num:
        print(2)
        raise Exception
    for contact in contacts:
        if contact.allowed_user.user == request.user:
            print(3)
            raise Exception
    Contact.objects.create(
        posting_id=posting,
        allowed_user=Profile.objects.get(user=request.user),
    )
    # 문자 보내기
    match_phone_number = posting.user_id.profile.phone_number
    content = ('<저기요> 게시한 포스팅에 ' + request.user.profile.user.username + '님이 매칭 신청을 했습니다!'
               + ' store: ' + posting.store_id.title )
    send_alarm_sms(match_phone_number, content)
    return redirect('core:home', univ_pk)


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
    # data = {
    #     'content': list()
    # }
    data = {}

    if kwd:
        all_tags = set(Tag.objects.all())
        tags_list = []
        menus_filtered = []
        for all_tag in all_tags:
            due1 = all_tag.posting_id.create_date + datetime.timedelta(minutes=all_tag.posting_id.timer)
            now1 = datetime.datetime.now()
            if due1 > now1:
                tags_list.append(all_tag.content)
        tags = list(set(tags_list))
        filtered_tags = []
        for tag in tags:
            if kwd in tag:
                # print(kwd)
                # print(tag)
                filtered_tags.append(tag)
        postings = Posting.objects.filter(menu__icontains=kwd, finished=False)
        for posting in postings:
            if not posting.finished:
                print(posting.menu)
                menus_filtered.append(posting.menu)
        data = {
            'filtered_tags': filtered_tags,
            'menus_filtered': menus_filtered
        }

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

        return render(request, 'core/choice_detail.html', {'category': c_page, 'stores': stores})


def new_test(request):
    cat_list = ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점']
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    stores_univ = Store.objects.filter(univ_id=profile.univ)
    stores = Store.objects.all()
    data = {
        'cat_list': cat_list,
        'stores': stores,
        'stores_univ': stores_univ
    }
    return render(request, 'core/new_test.html', data)


def menu_search(request, pk):
    if request.method == 'POST':
        kwd = request.POST['kwd']
        kwd_string = str(kwd)
        print(kwd_string)
        if request.user.is_authenticated:
            current_user = request.user
            profile = Profile.objects.get(user=current_user.id)
            univ = profile.univ
            contacts = Contact.objects.filter(allowed_user=profile)
            rooms = Room.objects.all()
            stores = Store.objects.filter(univ_id=pk)
            postings = []
            menus = []
            for store in stores:
                postings2 = Posting.objects.filter(store_id=store.id)
                postings3 = postings2.filter(menu=kwd_string)
                for posting in postings3:
                    postings.append(posting)
            tag_dic = {}
            for posting in postings:
                due = posting.create_date + datetime.timedelta(minutes=posting.timer)
                now = datetime.datetime.now()
                if due > now:
                    tags = []
                    tags += Tag.objects.filter(posting_id=posting.id)
                    posting.create_date_string = convert_date_PytoJs(str(posting.create_date))
                    tag_dic[posting] = tags
                    menus.append(posting.menu)
                else:
                    posting.finished = True
            all_tags = set(Tag.objects.all())
            tags_list = []
            for all_tag in all_tags:
                due1 = all_tag.posting_id.create_date + datetime.timedelta(minutes=all_tag.posting_id.timer)
                now1 = datetime.datetime.now()
                if due1 > now1:
                    tags_list.append(all_tag.content)
            rm_dup_tags = list(set(tags_list))
            data = {
                'contacts': contacts,
                'rooms': rooms,
                'postings': postings,
                'current_user': current_user.id,
                'univ': univ,
                'profile': profile,
                'categories': ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점'],
                'tag_dic': tag_dic,
                'rm_dup_tags': rm_dup_tags,
                'menus': menus,
            }
            return render(request, 'core/home.html', data)
        else:
            stores = Store.objects.filter(univ_id=pk)
            univ = Univ.objects.get(pk=pk)
            univs = Univ.objects.all()
            postings = []
            menus = []
            for store in stores:
                postings2 = Posting.objects.filter(store_id=store.id)
                postings3 = postings2.filter(menu=kwd_string)
                for posting in postings3:
                    postings.append(posting)
                    postings.append(posting)
            tag_dic = {}
            for posting in postings:
                due = posting.create_date + datetime.timedelta(minutes=posting.timer)
                now = datetime.datetime.now()
                if due > now:
                    tags = []
                    tags += Tag.objects.filter(posting_id=posting.id)
                    posting.create_date_string = convert_date_PytoJs(str(posting.create_date))
                    tag_dic[posting] = tags
                    menus.append(posting.menu)
                else:
                    posting.finished = True
            all_tags = set(Tag.objects.all())
            tags_list = []
            for all_tag in all_tags:
                due1 = all_tag.posting_id.create_date + datetime.timedelta(minutes=all_tag.posting_id.timer)
                now1 = datetime.datetime.now()
                if due1 > now1:
                    tags_list.append(all_tag.content)
            rm_dup_tags = list(set(tags_list))
            data = {
                'postings': postings,
                'univ': univ,
                'univs': univs,
                'categories': ['치킨', '피자양식', '중국집', '한식', '일식돈까스', '족발보쌈', '야식', '분식', '카페디저트', '편의점'],
                'tag_dic': tag_dic,
                'rm_dup_tags': rm_dup_tags,
                'menus': menus
            }
            return render(request, 'core/home.html', data)
