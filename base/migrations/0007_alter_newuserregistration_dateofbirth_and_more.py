# Generated by Django 4.1.2 on 2022-11-09 16:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0006_alter_newuserregistration_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newuserregistration",
            name="dateOfBirth",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="newuserregistration",
            name="mobile",
            field=models.BigIntegerField(blank=True, default=91),
        ),
    ]
