# Generated by Django 4.1.2 on 2022-11-06 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedbackmodel",
            name="comment",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
