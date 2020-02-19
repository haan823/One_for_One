# Generated by Django 2.2.9 on 2020-02-19 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthSms',
            fields=[
                ('phone_number', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('auth_number', models.IntegerField()),
            ],
            options={
                'db_table': 'auth_numbers',
            },
        ),
        migrations.CreateModel(
            name='Univ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('addr', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nickname', models.TextField(max_length=10)),
                ('phone_number', models.CharField(default='01000000000', max_length=20)),
                ('good_review', models.IntegerField(default=0)),
                ('bad_review', models.IntegerField(default=0)),
                ('univ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Univ')),
            ],
        ),
    ]
