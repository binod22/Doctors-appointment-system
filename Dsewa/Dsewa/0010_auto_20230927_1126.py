# Generated by Django 4.2.2 on 2023-09-27 11:26

from django.db import migrations,models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0009_add_unique_appointmentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
