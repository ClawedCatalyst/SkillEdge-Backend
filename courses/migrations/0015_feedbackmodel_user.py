# Generated by Django 4.1.3 on 2022-11-14 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0014_remove_feedbackmodel_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedbackmodel",
            name="user",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
