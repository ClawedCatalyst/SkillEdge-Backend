# Generated by Django 4.1.2 on 2022-11-09 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_squashed_0003_lessons"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedbackmodel",
            name="comment",
            field=models.CharField(default=" ", max_length=100),
        ),
    ]
