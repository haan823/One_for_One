from django.shortcuts import render

# from sms.models import OFO_user
# from sms.utils import send_matching_sms
#
#
# def send_sms(request):
#     user1 = OFO_user()
#     user1.phone = "01023071821"
#     send_matching_sms(user1)

from sms.utils import AuthSmsSendView


def send_sms(request):
    assv = AuthSmsSendView()
    assv.post(request)


def certificate_phone(request):
    return render(request, 'sms/certificate_phone.html')