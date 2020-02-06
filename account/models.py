from django.db import models
from django.contrib.auth.models import User

class Univ(models.Model):
    univ = models.TextField(max_length=255)

    def __str__(self):
        return self.univ

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.TextField(max_length=10)
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE)