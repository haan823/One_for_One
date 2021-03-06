from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import Univ


class Store(models.Model):
    logo = models.URLField()
    title = models.CharField(max_length=255, verbose_name='가게명')
    star = models.CharField(max_length=255, verbose_name='별점')
    min_price = models.CharField(max_length=255, verbose_name='최소주문금액')
    del_time = models.CharField(max_length=255, verbose_name='배달시간')
    store_url = models.URLField()
    cat_name = models.CharField(max_length=255, verbose_name='카테고리명')
    univ_id = models.ForeignKey(Univ, on_delete=models.CASCADE, verbose_name='대학', related_name='category', null=True)

    def __str__(self):
        return self.title


class Posting(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='posting', null=True)
    menu = models.CharField(max_length=255, null=True)
    price = models.IntegerField(null=True)
    max_num = models.IntegerField(null=True)
    now_num = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], default=1)
    timer = models.IntegerField(blank=True, null=True)
    finished = models.BooleanField(default=False)
    chat_created = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    create_date_string = models.CharField(max_length=255, blank=True, null=True)
    menu_change = models.CharField(max_length=255, null=True)
    together = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.store_id.title

    def posting_order(self):
        length = len(Posting.objects.all())
        return Posting.objects.order_by('-create_date').all()[:length]


class Tag(models.Model):
    posting_id = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name='tag')
    content = models.CharField(max_length=20)