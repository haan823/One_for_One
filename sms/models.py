from django.contrib.auth.models import User
from django.db import models


class AuthSms(models.Model):
    phone_number = models.CharField(max_length=20, primary_key=True)
    auth_number = models.IntegerField()

    class Meta:
        db_table = 'auth_numbers'
