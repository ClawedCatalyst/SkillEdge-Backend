# Generated by Django 4.1.2 on 2022-11-10 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0007_alter_lessons_length"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lessons",
            name="length",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
