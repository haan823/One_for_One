# import string
# import requests
# import json
# import os
#
# from random import random
#
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import HttpResponse
#
# from sms.models import OFO_user
#
#
# class SMSManager:
#     # todo: accesskey랑 발신번호 및 시크릿 키 초기화 필요
#     serviceId = "ncp:sms:kr:258123171330:oneforone"
#     access_key = "nyfwSNQgWpo8zxTFHW5S"
#     secret_key = "a5cc3ea4f2c1479a9aa1e3342d7addbe"
#     _from = "One_For_One"
#     url = "https://api-sens.ncloud.com/v1/sms/services/{}/messages".format(serviceId)
#     headers = {
#         'Content-Type': 'application/json; charset=utf-8',
#         'x-ncp-auth-key': {access_key},
#         'x-ncp-service-secret': {secret_key},
#     }
#
#     def __init__(self, user):
#         self.user = user
#         self.confirm_key = ""
#         self.body = {
#             "type": "SMS",
#             "countryCode": "82",
#             "from": self._from,
#             "to": [],
#             "subject": "",
#             "content": ""
#         }
#
#     def set_matching_content(self):
#         self.body['content'] = "1:1 배달매칭이 성공했습니다. OneForOne 웹사이트를 방문해주세요."
#
#     # def send_sms(self):
#     #     if self.user:
#     #         self.body['to'].append(self.user.phone)
#     #     res = requests.post(self.url, headers=self.headers,
#     #                         data=json.dumps(self.body, ensure_ascii=False).encode('utf-8'))
#     #     return res
#
#
# def send_matching_sms(user):
#     sms_manager = SMSManager(user)
#     # sms_manager.__init__(user)
#     print(user)
#     sms_manager.set_matching_content()
#     sms_manager.body['to'].append(sms_manager.user.phone)
#     requests.post(sms_manager.url, headers=sms_manager.headers,
#                   data=json.dumps(sms_manager.body, ensure_ascii=False).encode('utf-8'))
#     return HttpResponse(202)
import json
from random import randint

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from sms.models import AuthSms

serviceId = "ncp:sms:kr:258123171330:oneforone"
SMS_ACCESS_KEY_ID = "nyfwSNQgWpo8zxTFHW5S"
SMS_SERVICE_SECRET = "a5cc3ea4f2c1479a9aa1e3342d7addbe"
SMS_SEND_PHONE_NUMBER = "01023071821"
SMS_URL = "https://api-sens.ncloud.com/v1/sms/services/{}/messages".format(serviceId)


class AuthSmsSendView(View):
    # 실제 문자를 보내주는 메서드
    def send_sms(self, phone_number, auth_number):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-auth-key': f'{SMS_ACCESS_KEY_ID}',
            'x-ncp-service-secret': f'{SMS_SERVICE_SECRET}',
        }

        data = {
            'type': 'SMS',
            'contentType': 'COMM',
            'countryCode': '82',
            'from': f'{SMS_SEND_PHONE_NUMBER}',
            'to': [
                f'{phone_number}',
            ],
            'content': f'인증번호 [{auth_number}]'
        }

        requests.post(SMS_URL, headers=headers, json=data)

    def post(self, request, phone_number):
        try:
            input_phone_number = phone_number
            created_auth_number = randint(1000, 10000)
            exist_phone_number = AuthSms.objects.get(phone_number=input_phone_number)
            exist_phone_number.auth_number = created_auth_number
            exist_phone_number.save()

            self.send_sms(phone_number=input_phone_number, auth_number=created_auth_number)
            context = {'auth_number': created_auth_number }
            return render(request, 'sms/certificate_phone.html', context)

        except AuthSms.DoesNotExist:
            AuthSms.objects.create(
                phone_number=input_phone_number,
                auth_number=created_auth_number
            ).save()

            self.send_sms(phone_number=input_phone_number, auth_number=created_auth_number)
            return JsonResponse({'message': 'SUCCESS'}, status=200)
