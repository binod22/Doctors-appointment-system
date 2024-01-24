# Generated by Django 4.2.2 on 2023-07-04 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_rename_first_name_doctor_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='bloodgroup',
        ),
        migrations.AddField(
            model_name='doctor',
            name='doc_license_image',
            field=models.ImageField(blank=True, null=True, upload_to='doc_license_image'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='qualification',
            field=models.CharField(default='MBBS', max_length=15, null='False'),
            preserve_default='False',
        ),
    ]