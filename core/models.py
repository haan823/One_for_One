from django.db import models

class Category(models.Model):
    title = models.CharField()

class Store(models.Model):
    logo = models.URLField()
    title = models.CharField(max_length=255)
    star = models.CharField(max_length=255)
    min_price = models.PositiveIntegerField()
    del_time = models.PositiveIntegerField()
    store_url = models.URLField()

    def __str__(self):
        return self.title