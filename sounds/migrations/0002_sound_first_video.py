# Generated by Django 3.0.8 on 2020-07-25 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sound',
            name='first_video',
            field=models.FileField(blank=True, null=True, upload_to='uploads/videos/'),
        ),
    ]