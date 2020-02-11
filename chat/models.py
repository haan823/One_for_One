from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from core.models import Posting

class Contact(models.Model):
    user = models.ForeignKey(User, related_name = 'friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    author = models.ForeignKey(User, related_name = 'author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]


class Room(models.Model):
    Posting_id = models.OneToOneField(Posting, on_delete=models.CASCADE, primary_key=True)
    allowed_users = models.ManyToManyField(Contact, related_name = 'chats')
    now_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    match_finished = models.BooleanField(default=True)

    def __str__(self):
         return "{}".format(self.pk)



# class Room(models.Model):
#     room_name = models.TextField()
#     allowed_users = model.OneToManyField(User)
