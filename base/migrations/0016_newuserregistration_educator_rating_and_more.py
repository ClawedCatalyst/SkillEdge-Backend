# Generated by Django 4.1.3 on 2022-11-14 19:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0015_alter_newuserregistration_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="newuserregistration",
            name="educator_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="newuserregistration",
            name="is_certified_educator",
            field=models.BooleanField(default=False),
        ),
    ]
