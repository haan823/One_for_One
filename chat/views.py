from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import json

from chat.models import Room, Contact
from core.models import Posting


def index(request):
    return render(request, 'chat/index.html')


@login_required
def room(request, pk):
    room = Room.objects.get(pk=pk)
    posting = Posting.objects.get(pk=pk)
    contacts = Contact.objects.filter(room_id=pk)
    allowed_users = [contact.allowed_user.username for contact in contacts]
    if room.now_number == room.Posting_id.max_num:
        raise PermissionDenied
    if request.user.username not in allowed_users:
        raise PermissionDenied
    return render(request, 'chat/room.html', {
        'room': room,
        'posting': posting,
        'username': mark_safe(json.dumps(request.user.username)),
        'allowed_users': allowed_users
    })


def Create_Room(request, pk):
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
