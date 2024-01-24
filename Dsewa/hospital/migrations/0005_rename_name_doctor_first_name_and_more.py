# Generated by Django 4.2.2 on 2023-07-02 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_doctor_doc_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='doctor',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]