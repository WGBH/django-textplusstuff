Installation Instructions
=========================

Installation is easy with ``pip``:

1. Installation is easy with `pip <https://pypi.python.org/pypi/pip>`__:

    .. code-block:: bash

        $ pip install django-textplusstuff

    .. note:: ``django-textplusstuff`` will not install ``django``.

2. Add required settings:

    Add `textplusstuff` to `INSTALLED_APPS`:

    .. code-block:: python

        INSTALLED_APPS = (
            # Other apps here
            'rest_framework',
            'textplusstuff',
        )

    Add the TEXTPLUSSTUFF_STUFFGROUPS setting with at least one StuffGroup. It can be named whatever you like (the one below is just 'example'):

    .. code-block:: python

        TEXTPLUSSTUFF_STUFFGROUPS = {
            'example': {
                'name': 'Example',
                'description': "This is an example of a StuffGroup!"
            },
        }

    .. note:: StuffGroups are used to organize Stuff in the upcoming editor tool and are required when you register Stuff.

3. Add textplusstuff-required bits to your project's base `urls.py`:

    .. code-block:: python
        :emphasize-lines: 6,9,16

        # Base project urls.py
        from django.conf.urls import patterns, include, url
        from django.contrib import admin

        # Importing required textplusstuff bits
        from textplusstuff.registry import stuff_registry, findstuff

        # Firing off the textplusstuff discovery engine
        findstuff()

        urlpatterns = patterns(
            '',
            # Admin URLs
            url(r'^admin/', include(admin.site.urls)),
            # textplusstuff URLs
            url(r'^textplusstuff/', include(stuff_registry.urls))
        )
