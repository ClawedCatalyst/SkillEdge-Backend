# Generated by Django 4.1.2 on 2022-11-05 12:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="newuserregistration",
            name="interest",
            field=models.ManyToManyField(to="base.interests"),
        ),
    ]
