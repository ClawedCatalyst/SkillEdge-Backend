# Generated by Django 4.1.2 on 2022-11-09 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0006_alter_feedbackmodel_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedbackmodel",
            name="user",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]