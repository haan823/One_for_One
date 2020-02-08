from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    rooms  = Room.objects.filter(room_name=room_name)
    if len(rooms) == 0:
        raise Exception
    room = rooms[0]
    if request.user.id not in [ user.id for user in room.allowed_users]:
        raise Exception

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username' : mark_safe(json.dumps(request.user.username)),
    })
