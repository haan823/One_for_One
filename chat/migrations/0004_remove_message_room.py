# Generated by Django 2.2.9 on 2020-02-11 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20200211_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='Room',
        ),
    ]
