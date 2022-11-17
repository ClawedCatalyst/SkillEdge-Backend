
from django.db import migrations, models
import django.db.models.deletion
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):

    dependencies = [
        ('courses','0015_feedbackmodel_user'),
    ]

    operations = [
        TrigramExtension(),
    ]