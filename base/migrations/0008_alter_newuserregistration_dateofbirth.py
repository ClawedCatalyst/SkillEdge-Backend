# Generated by Django 4.1.2 on 2022-11-09 16:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0007_alter_newuserregistration_dateofbirth_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newuserregistration",
            name="dateOfBirth",
            field=models.DateField(null=True),
        ),
    ]
