from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import json

from account.models import Profile
from chat.models import Room, Contact
from core.models import Posting


def index(request):
    return render(request, 'chat/index.html')


@login_required
def room(request, pk):
    now_user = Profile.objects.get(user=request.user)
    room = Room.objects.get(pk=pk)
    posting = Posting.objects.get(pk=pk)
    contacts = Contact.objects.filter(room_id=pk)
    allowed_users = [contact.allowed_user.user for contact in contacts if contact.finished==False]
    contact = contacts.get(allowed_user=now_user)
    # if room.now_number  room.Posting_id.max_num:
    #     raise PermissionDenied
    if request.user not in allowed_users:
        raise PermissionDenied
    return render(request, 'chat/room.html', {
        'room': room,
        'posting': posting,
        'username': mark_safe(json.dumps(request.user.username)),
        'allowed_users': allowed_users,
        'now_user': request.user
    })


def create_Room(request, pk):
    posting = Posting.objects.get(pk=pk)
    room = Room.objects.create(
        Posting_id=posting,
    )
    room.save()
    contact = Contact.objects.create(
        room_id=room,
        allowed_user=request.user
    )
    contact.save()
    return redirect('chat:room', room.pk)


# def Enter_Room(request, pk):
#     room = Room.objects.get(pk=pk)
#     try:
#         room.now_number = room.now_number+1
#     except:
#         print()
#     contact = Contact.objects.create(
#         room_id=room,
#         allowed_user=request.user
#     )
#     contact.save()
#     return redirect('chat:room', room.pk)

def matching_finished(request, pk):
    posting = Posting.objects.get(pk=pk)
    if posting.finished == True:
        raise Exception
    else:
        posting.finished = True
        posting.save()
    return redirect('chat:room', posting.pk)


def re_match(request, pk):
    posting = Posting.objects.get(pk=pk)
    if posting.finished == False:
        raise Exception
    else:
        posting.finished = False
        posting.save()
    return redirect('chat:room', posting.pk)


def review(request, pk):
    now_user = Profile.objects.get(pk=request.user.pk)
    posting = Posting.objects.get(pk=pk)
    contacts = Contact.objects.filter(room_id=pk)
    allowed_users = [contact.allowed_user.user for contact in contacts]
    return render(request, 'chat/review.html', {
        'now_user': now_user,
        'posting': posting,
        'allowed_users': allowed_users
    })

def update_review(request, pk):
    now_user = Profile.objects.get(pk=request.user.pk)
    posting = Posting.objects.get(pk=pk)
    room = Room.objects.get(pk=pk)
    contacts = Contact.objects.filter(room_id=pk)
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
    if room.now_number>1:
        contact = contacts.get(allowed_user=now_user)
        print(contact)
        contact.finished = True
        contact.save()
        room.now_number-=1
        room.save()
    elif room.now_number==1:
        room.delete()
        contacts.delete()
        posting.finished=True
        posting.save()
    return render(request, 'chat/update_review.html')


def delete_chatting(request, pk):
    room = Room.objects.get(pk=pk)
    room.delete()
    return redirect('core:home', room.pk)


def delete_contact(request, pk):
    user_pk = request.GET['user_pk']
    contact = Contact.objects.filter(room_id=pk).get(allowed_user=user_pk)
    contact.delete()
    return render(request, 'chat/room.html')
