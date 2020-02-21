from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import json

from account.models import Profile
from account.utils import send_alarm_sms
from chat.models import Room, Contact, Message
from core.models import Posting


def index(request):
    return render(request, 'chat/index.html')


@login_required
def room(request, pk):
    now_user = Profile.objects.get(user=request.user)
    room = Room.objects.get(pk=pk)
    posting = Posting.objects.get(pk=pk)
    contacts = Contact.objects.filter(posting_id=pk)
    allowed_users = [contact.allowed_user.user for contact in contacts if contact.accepted==True]
    # if room.now_number  room.Posting_id.max_num:
    #     raise PermissionDenied
    if request.user not in allowed_users:
        return render(request, 'chat/already_out.html')
    else:
        return render(request, 'chat/room.html', {
            'room': room,
            'posting': posting,
            'username': mark_safe(json.dumps(request.user.username)),
            'allowed_users': allowed_users,
            'now_user': request.user
        })


def create_Room(request, pk):
    posting = Posting.objects.get(pk=pk)
    posting.chat_created = True
    posting.save()
    room = Room.objects.create(
        posting_id=posting,
    )
    room.save()
    contacts = Contact.objects.filter(posting_id = posting)
    for contact in contacts:
        contact.accepted = True
        contact.save()
    # 문자 다 보내기
    for contact in contacts:
        content = f'<저기요> 채팅방이 개설되었습니다. store: ' + posting.store_id.title
        send_alarm_sms(contact.allowed_user.phone_number, content)
        print(content)
    return redirect('core:my_page')

def room_finished(request, pk):
    room = Room.objects.get(pk=pk)
    if room.match_finished== True:
        raise Exception
    else:
        room.match_finished = True
        room.save()
    return redirect('chat:room', room.pk)

def review(request, pk):
    now_user = Profile.objects.get(pk=request.user.pk)
    posting = Posting.objects.get(pk=pk)
    room = Room.objects.get(pk=pk)
    contacts = Contact.objects.filter(posting_id=pk)
    allowed_users = [contact.allowed_user.user for contact in contacts]
    return render(request, 'chat/review.html', {
        'room': room,
        'now_user': now_user,
        'posting': posting,
        'allowed_users': allowed_users
    })

def update_review(request, pk):
    now_user = Profile.objects.get(pk=request.user.pk)
    posting = Posting.objects.get(pk=pk)
    contacts = Contact.objects.filter(posting_id=pk)
    allowed_users = [contact.allowed_user for contact in contacts]
    for allowed_user in allowed_users:
        allowed_user_pk= str(allowed_user.pk)
        get_review = request.GET.get(allowed_user_pk)
        if get_review == 'good':
            allowed_user.good_review +=1
            allowed_user.save()
        elif get_review == 'bad':
            allowed_user.bad_review +=1
            allowed_user.save()
    contact = contacts.get(allowed_user=now_user)
    contact.finished = True
    contact.save()
    posting.now_num-=1
    posting.save()
    if posting.now_num == 0:
        posting.finished = True
        posting.save()
    return render(request, 'chat/update_review.html')

def delete_contact(request, pk):
   user_pk = request.GET['user_pk']
   contact = Contact.objects.filter(room_id=pk).get(allowed_user=user_pk)
   contact.delete()
   return redirect('chat:room', pk)
