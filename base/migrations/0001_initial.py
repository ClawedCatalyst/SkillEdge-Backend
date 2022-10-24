# Generated by Django 4.1.2 on 2022-10-24 22:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NewUserRegistration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="email address"
                    ),
                ),
                ("name", models.CharField(default=None, max_length=150)),
                (
                    "user_name",
                    models.CharField(
                        blank=True, default="none", max_length=150, null=True
                    ),
                ),
                ("otp", models.CharField(blank=True, max_length=4, null=True)),
                ("is_verified", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OTP",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("verifyEmail", models.EmailField(default=True, max_length=255)),
                (
                    "time_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
    ]
