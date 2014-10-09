from django.core.exceptions import ImproperlyConfigured


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class NonExistantGroup(Exception):
    pass


class InvalidRendition(Exception):
    pass


class InvalidRenditionType(Exception):
    pass


class InvalidToken(Exception):
    pass


class ImproperlyConfiguredStuff(ImproperlyConfigured):
    pass


class MissingRendition(Exception):
    pass
