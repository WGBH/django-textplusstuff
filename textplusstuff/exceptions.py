from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class NonExistentGroup(Exception):
    pass


class InvalidRenderOption(Exception):
    pass


class InvalidRendition(Exception):
    pass


class InvalidRenditionType(Exception):
    pass


class InvalidToken(Exception):
    pass


class ImproperlyConfiguredStuff(ImproperlyConfigured):
    pass


class MalformedToken(Exception):
    pass


class MissingRendition(Exception):
    pass
