# Generated by Django 3.0.8 on 2020-09-05 14:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_is_pornographic'),
        ('usermodule', '0004_auto_20200806_1324'),
        ('favorites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.PostCategory')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermodule.Profile')),
            ],
            options={
                'unique_together': {('profile', 'category')},
            },
        ),
    ]