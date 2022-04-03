# Generated by Django 3.2.7 on 2021-10-27 14:06

from django.db import migrations, models
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_photo_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(height_field='image_height', upload_to=photos.models.photo_directory_path, width_field='image_width'),
        ),
    ]
