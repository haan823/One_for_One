# Generated by Django 2.2.9 on 2020-02-06 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default='01000000000', max_length=20),
        ),
    ]
