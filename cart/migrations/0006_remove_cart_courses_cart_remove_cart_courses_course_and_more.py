# Generated by Django 4.1.2 on 2022-11-09 04:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0005_rename_student_mail_cart_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart_courses",
            name="cart",
        ),
        migrations.RemoveField(
            model_name="cart_courses",
            name="course",
        ),
        migrations.DeleteModel(
            name="cart",
        ),
        migrations.DeleteModel(
            name="cart_courses",
        ),
    ]
