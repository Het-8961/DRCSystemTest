# Generated by Django 4.0.5 on 2022-07-05 08:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_signup_isblocked_signup_lastloginattemptedtime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='lastLoginAttemptedTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 13, 37, 27, 379748)),
        ),
    ]