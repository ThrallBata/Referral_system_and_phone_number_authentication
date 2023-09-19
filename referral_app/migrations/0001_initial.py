# Generated by Django 4.2.4 on 2023-09-17 01:24

import django.core.validators
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+79*********'.", regex='^(\\+7|8).*?(\\d{2,3}).*?(\\d{2,3}).*?(\\d{2}).*?(\\d{2})$')], verbose_name='Номер телефона')),
                ('invite_code', models.CharField(max_length=6, verbose_name='Код приглашения')),
                ('inviter', models.CharField(max_length=6, null=True, verbose_name='Код пригласившего')),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
