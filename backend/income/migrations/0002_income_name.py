# Generated by Django 4.2.5 on 2023-09-27 13:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("income", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="income",
            name="name",
            field=models.CharField(default="New income", max_length=255),
        ),
    ]
