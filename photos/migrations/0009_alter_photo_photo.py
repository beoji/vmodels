# Generated by Django 3.2.7 on 2021-10-31 11:05

from django.db import migrations, models
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0008_alter_photo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(height_field='height', upload_to=photos.models.photo_directory_path, width_field='width'),
        ),
    ]