# -*- coding: utf-8 -*-

import datetime
import shutil
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
    timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%d_%m_%Y_%H_%M_%S')
    uuid_user = instance.uuid
    user_folder = '{0}{1}/{2}'.format(settings.MEDIA_ROOT,
                                      uuid_user,
                                      'image_profile')
    if user_folder in instance.photo_profile.path:
        try:
            shutil.rmtree(user_folder)
        except OSError:
            pass
    return '{0}/{1}/{2}_{3}.{4}'.format(uuid_user,
                                        'image_profile',
                                        'profile',
                                        timestamp,
                                        filename.split('.')[-1])


class User(AbstractUser):

    photo_profile = models.ImageField(_('Photo'), upload_to=user_directory_path, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=256, unique=True, null=True)
    country = CountryField(_('Country'), blank=True, blank_label=_('Country'))
    email = models.EmailField(_('email address'), blank=True, unique=True)
    preferred_language = models.CharField(_('Preferred Language'), null=True, blank=True, max_length=100, choices=settings.LANGUAGES)
