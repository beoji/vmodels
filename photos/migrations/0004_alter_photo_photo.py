# Generated by Django 3.2.7 on 2021-10-27 14:07

from django.db import migrations, models
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_alter_photo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to=photos.models.photo_directory_path),
        ),
    ]