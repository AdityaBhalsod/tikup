# Generated by Django 3.0.8 on 2020-07-25 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermodule', '0002_auto_20200725_0504'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='display_pic',
            field=models.ImageField(blank=True, null=True, upload_to='user/image/'),
        ),
    ]