# Generated by Django 4.1.3 on 2022-11-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0020_otp_is_verified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="interests",
            name="interest",
            field=models.BooleanField(max_length=50, null=True),
        ),
    ]
