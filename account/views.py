from random import randint

from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.core.serializers import json
from django.db.models.functions import datetime
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import random
from django.views import View

# from core.models import Category
from .models import Profile, Univ, AuthSms

from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.

def randstr(length):
    rstr = "0123456789abcdefghijklnmopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ"
    rstr_len = len(rstr) - 1
    result = ""
    for i in range(length):
        result += rstr[random.randint(0, rstr_len)]
    return result


def home(request):
    return render(request, 'home.html')


def goto_signup(request):
    if request.method == 'POST':
        univ = request.POST['univ']
        return redirect(reverse('account:signup', args=[univ]))
    else:
        univs = Univ.objects.all()
        data = {
            'univs': univs
        }
        return render(request, 'choice_univ.html', data)


def signup(request, pk):
    univ = Univ.objects.get(pk=pk)
    if request.method == "POST":
        user_authsms = AuthSms.objects.get(phone_number=request.POST['phone_number'])
        if int(request.POST['user_auth_number']) != int(user_authsms.auth_number):
            UNIV_DOMAIN_MAPPING = {
                '서울대학교': 'snu.ac.kr',
                '성균관대학교': 'g.skku.edu',
                '이화여자대학교': 'ewhain.net',
                '홍익대학교': 'mail.hongik.ac.kr',
            }
            context = {
                'message': '비밀번호가 일치하지 않습니다.',
                'pk': pk,
                'univ': univ,
                'email_domain': UNIV_DOMAIN_MAPPING.get(univ.name),

                'de_username': request.POST["username"],
                'de_password1': request.POST["password1"],
                'de_password2': request.POST["password2"],
                'de_email_id': request.POST["email_id"],
                'de_nickname': request.POST["nickname"],
                'de_phone_number': request.POST['phone_number']
            }
            return render(request, 'signup.html', context)

        if request.POST["password1"] == request.POST["password2"]:
            email = request.POST['email_id'] + '@' + request.POST['email_domain']
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"],
                last_name=randstr(50),
                email=request.POST["email_id"]
            )
            user.is_active = False
            user.save()
            nickname = request.POST["nickname"]
            phone_number = request.POST['phone_number']
            profile = Profile(
                user=user,
                nickname=nickname,
                univ=univ,
                phone_number=phone_number,
            )
            profile.save()
            auth.login(request, user)
            mail = EmailMessage('One for One 회원가입 인증 메일입니다.',
                                'url을 클릭하면 인증됩니다.' + 'http://127.0.0.1:8000/account/active/' + user.last_name,
                                to=[email])
            mail.send()
            return render(request, 'notify.html')
        else:
            return render(request, 'signup.html', {'message': '비밀번호가 일치하지 않습니다.', 'pk': request.GET.pk})
    else:
        UNIV_DOMAIN_MAPPING = {
            '서울대학교': 'snu.ac.kr',
            '성균관대학교': 'g.skku.edu',
            '이화여자대학교': 'ewhain.net',
            '홍익대학교': 'mail.hongik.ac.kr',
        }

        profiles = Profile.objects.all()
        data = {
            'univ': univ,
            'email_domain': UNIV_DOMAIN_MAPPING.get(univ.name),

            'username_list': [profile.user.username for profile in profiles],
            'nickname_list': [profile.nickname for profile in profiles],
            'phone_number_list': [profile.phone_number for profile in profiles],
            'email_id_list': [profile.user.email for profile in profiles],

            'de_username': "",
            'de_password1': "",
            'de_password2': "",
            'de_email_id': "",
            'de_nickname': "",
            'de_phone_number': "",
        }
        return render(request, 'signup.html', data)


def login(request):
    if request.method == "POST":
        username = request.POST["id"]
        password = request.POST["password"]
        # 해당 user가 있으면 username, 없으면 None
        user = auth.authenticate(request, username=username, password=password)
        profile = Profile.objects.get(user=user)
        univ = profile.univ
        if user is not None:
            auth.login(request, user)
            return redirect(reverse('core:home', args=[univ.id]))
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect("account:login")


def user_active(request, token):
    user = User.objects.get(last_name=token)
    user.is_active = True
    user.last_name = ''
    user.save()
    message = "이메일이 인증되었습니다."
    return render(request, 'signup_complete.html', {'message': message})


def send_sms(request, pk):
    from account.utils import AuthSmsSendView
    assv = AuthSmsSendView()
    user_phone_number = request.POST['user_phone_number']
    assv.post(request, user_phone_number)
    return render(request, 'test3.html')


def test(request):
    return render(request, 'test3.html', {'count': 6})


def auth_check(request, pk):
    user_authsms = AuthSms.objects.get(phone_number=request.POST['user_phone_number'])
    if int(request.POST['user_auth_number']) == int(user_authsms.auth_number):
        print(request.POST['user_auth_number'])
        print(user_authsms.auth_number)
        return render(request, 'test3.html')
    else:
        return None
