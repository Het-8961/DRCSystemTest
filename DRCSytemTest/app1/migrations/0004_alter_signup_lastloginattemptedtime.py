# Generated by Django 4.0.5 on 2022-07-05 08:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_signup_lastloginattemptedtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='lastLoginAttemptedTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 13, 37, 31, 879418)),
        ),
    ]