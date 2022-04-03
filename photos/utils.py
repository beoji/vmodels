from django.core.files.base import ContentFile
from django.conf import settings

from PIL import Image
from io import BytesIO

import os
import uuid


def make_thumbnail(photo):
    ratio = photo.width / photo.height
    print(f'url = {photo.photo}, height = {photo.height}, width = {photo.width}, ratio = {ratio}')
    try:
        path = settings.MEDIA_ROOT + '/' + str(photo.photo)
        # print(path)
        img = Image.open(path)
        # folder_path = settings.MEDIA_ROOT + '/' + photo.profile.user.username + '/thumbnails/'
        # os.makedirs(folder_path, exist_ok=True)
        # file_path = folder_path + str(uuid.uuid4()) + photo.file_extension
        # print(file_path)
        # img.thumbnail((256, 256))
        i = img.resize((256,img.height*256//img.width), Image.ANTIALIAS)
        buffer = BytesIO()
        i.save(fp=buffer, format='JPEG')
        return ContentFile(buffer.getvalue())
        # i.save(file_path)
        # i.show()
    except Exception as e:
        print(e.args)
