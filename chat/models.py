from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from account.models import Profile
from core.models import Posting


class Room(models.Model):
    posting_id = models.OneToOneField(Posting, on_delete=models.CASCADE, primary_key=True)
    now_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], default=1)
    match_finished = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.pk)


class Contact(models.Model):
    posting_id = models.ForeignKey(Posting, on_delete=models.CASCADE)
    allowed_user = models.ForeignKey(Profile, related_name='allowed_user', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    finished = models.BooleanField(default= False)

    def __str__(self):
        return self.allowed_user.user.username + str(self.posting_id.pk)


class Message(models.Model):
    room_id = models.PositiveIntegerField()
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        length = len(Message.objects.all())
        return Message.objects.order_by('-timestamp').all()[:length]

