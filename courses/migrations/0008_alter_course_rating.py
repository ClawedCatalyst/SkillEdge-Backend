# Generated by Django 4.1.2 on 2022-11-02 14:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0007_alter_course_educator_mail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="rating",
            field=models.FloatField(
                default=0, validators=[django.core.validators.MaxValueValidator(5)]
            ),
        ),
    ]