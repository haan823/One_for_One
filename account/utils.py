from random import randint

import requests

from django.views import View

from account.models import AuthSms

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
            'content': f'OneforOne 서비스의 인증번호는 [{auth_number}]입니다.'
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
        except AuthSms.DoesNotExist:
            AuthSms.objects.create(
                phone_number=input_phone_number,
                auth_number=created_auth_number,
            ).save()

            self.send_sms(phone_number=input_phone_number, auth_number=created_auth_number)
