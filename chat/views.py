from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from chat.models import Room


def index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request,pk):
    room = Room.objects.get(pk=pk)
    allowed_users = list(map(str, room.allowed_users.all()))
    print(room.now_number)
    # if room.now_number == room.Posting_id.max_num:
    #     raise PermissionDenied
    if request.user.username not in allowed_users:
        raise PermissionDenied
    return render(request, 'chat/room.html', {
        'room': room,
        'username' : mark_safe(json.dumps(request.user.username)),
        'allowed_users': allowed_users
    })


