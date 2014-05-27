from django.core.exceptions import ImproperlyConfigured


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class NonExistantGroup(Exception):
    pass


class InvalidRenditionType(Exception):
    pass


class ImproperlyConfiguredStuff(ImproperlyConfigured):
    pass
