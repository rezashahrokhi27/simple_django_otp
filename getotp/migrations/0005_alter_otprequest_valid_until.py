# Generated by Django 4.2 on 2023-04-09 19:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getotp', '0004_alter_otprequest_valid_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='valid_until',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 21, 19, 16, 32, 921830, tzinfo=datetime.timezone.utc)),
        ),
    ]
