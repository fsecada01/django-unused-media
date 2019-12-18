# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.validators import URLValidator


def get_path():
    '''A simple python script to validate MEDIA_URL. If var is local,
    validation will fail and will default to MEDIA_ROOT. Else, var will be
    set to MEDIA_URL.
    This should make the script compliant with cloud storage instances.
    '''
    path = settings.MEDIA_URL
    val = URLValidator()
    try:
        val(path)
    except ValidationError:
        path = settings.MEDIA_ROOT
    return path


def remove_media(files):
    """
        Delete file from media dir
    """
    for filename in files:
        os.remove(os.path.join(get_path(), filename))


def remove_empty_dirs(path=None):
    """
        Recursively delete empty directories; return True if everything was deleted.
    """

    if not path:
        path = get_path()

    if not os.path.isdir(path):
        return False

    listdir = [os.path.join(path, filename) for filename in os.listdir(path)]

    if all(list(map(remove_empty_dirs, listdir))):
        os.rmdir(path)
        return True
    else:
        return False
