from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import Univ


# class Category(models.Model):
#     cat_name = models.CharField(max_length=255, verbose_name='카테고리명')
#     univ_cat = models.ManyToManyField(Univ)
#     # univ_id = models.ForeignKey(Univ, on_delete=models.CASCADE, verbose_name='대학', related_name='category')
#
#     def __str__(self):
#         return self.cat_name
class Store(models.Model):
    logo = models.URLField()
    title = models.CharField(max_length=255, verbose_name='가게명')
    star = models.CharField(max_length=255, verbose_name='별점')
    min_price = models.CharField(max_length=255, verbose_name='최소주문금액')
    del_time = models.CharField(max_length=255, verbose_name='배달시간')
    store_url = models.URLField()
    cat_name = models.CharField(max_length=255, verbose_name='카테고리명')
    univ_id = models.ForeignKey(Univ, on_delete=models.CASCADE, verbose_name='대학', related_name='category', null=True)
    # category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='카테고리명', related_name='store', null=True)
    # cat_name = models.CharField(max_length=255, verbose_name='카테고리_이름')
    # univ_name = models.CharField(max_length=255, verbose_name='학교_이름')

    def __str__(self):
        return self.title


class Posting(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='posting')
    menu = models.CharField(max_length=255)
    price = models.IntegerField()
    max_num = models.IntegerField()
    timer = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    # finished = models.BooleanField(default=False)


class Tag(models.Model):
    posting_id = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name='tag')
    content = models.CharField(max_length=20)


# class Crawling(models.Model):
#     store_url = models.URLField(null=True, blank=True)
#     logo = models.URLField(null=True, blank=True)
#     title = models.CharField(max_length=255, verbose_name='가게명', null=True, blank=True)
#     star = models.CharField(max_length=255, verbose_name='별점', null=True, blank=True)
#     min_price = models.CharField(max_length=255, verbose_name='최소주문금액', null=True, blank=True)
#     del_time = models.CharField(max_length=255, verbose_name='배달시간', null=True, blank=True)
#     review = models.PositiveIntegerField(null=True)
#
#     def __str__(self):
#         return self.title