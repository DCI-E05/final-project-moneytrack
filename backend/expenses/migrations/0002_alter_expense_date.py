# Generated by Django 4.2.5 on 2023-09-27 13:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]