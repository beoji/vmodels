# Generated by Django 3.2.7 on 2021-10-29 11:58

from django.db import migrations, models
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_auto_20211028_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='thumbnail',
            field=models.ImageField(height_field='height', null=True, width_field='width'),
        ),
    ]
