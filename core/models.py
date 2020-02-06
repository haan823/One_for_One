from django.contrib.auth.models import User
from django.db import models



class Univ(models.Model):
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='카테고리명')
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE, verbose_name='대학', related_name='category')

    def __str__(self):
        return self.name


class Store(models.Model):
    logo = models.URLField()
    title = models.CharField(max_length=255, verbose_name='가게명')
    star = models.CharField(max_length=255, verbose_name='별점')
    min_price = models.PositiveIntegerField(verbose_name='최소주문금액')
    del_time = models.PositiveIntegerField(verbose_name='배달시간')
    store_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='카테고리명', related_name='store')

    def __str__(self):
        return self.title