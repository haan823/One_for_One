from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import Univ


class Category(models.Model):
    cat_name = models.CharField(max_length=255, verbose_name='카테고리명')
    univ_id = models.ForeignKey(Univ, on_delete=models.CASCADE, verbose_name='대학', related_name='category')

    def __str__(self):
        return self.name


class Store(models.Model):
    logo = models.URLField()
    title = models.CharField(max_length=255, verbose_name='가게명')
    star = models.CharField(max_length=255, verbose_name='별점')
    min_price = models.PositiveIntegerField(verbose_name='최소주문금액')
    del_time = models.PositiveIntegerField(verbose_name='배달시간')
    store_url = models.URLField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='카테고리명', related_name='store')

    def __str__(self):
        return self.title


class Posting(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='posting')
    menu = models.CharField(max_length=255)
    price = models.IntegerField()
    max_num = models.IntegerField()
    timer = models.DateTimeField(auto_now_add=False, blank=True, null=True)


class Tag(models.Model):
    posting_id = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name='tag')
    content = models.CharField(max_length=20)