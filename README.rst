====================
django-textplusstuff
====================

.. image:: https://travis-ci.org/WGBH/django-textplusstuff.svg?branch=master
    :target: https://travis-ci.org/WGBH/django-textplusstuff
    :alt: Travis CI Status

.. image:: https://img.shields.io/coveralls/WGBH/django-textplusstuff.svg?style=flat
    :target: https://coveralls.io/r/WGBH/django-textplusstuff
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/django-textplusstuff.svg?style=flat
    :target: https://pypi.python.org/pypi/django-textplusstuff/
    :alt: Latest Version

----

About
=====

Summary
-------

A django field that makes it easy to intersperse 'stuff' into blocks of text.

A Flexible Interface
````````````````````

``django-textplusstuff`` provides a simple interface for returning the contents of your field however you like: as either markdown-flavored text, valid HTML markup (with or without 'stuff' interspersed) or even plain text (with all markdown formatting removed).

Keep Track of Your Content
``````````````````````````

``django-textplusstuff`` also keeps track of which model instances are associated within each TextPlusStuffField (via the `TextPlusStuffLink` model) so you can see where all your textplusstuff-integrated content is used across your django project.

Easy Integration
````````````````

Registering existing models for use in TextPlusStuffFields is as easy as integrating a model into the admin.

Designer/Front-End Developer Friendly
`````````````````````````````````````

Each model registered with ``django-textplusstuff`` can have as many 'renditions' as you like which keeps business logic DRY while enabling designers and front-end developers to have control over how content is displayed.

Compatibility
-------------

| Version 0.7 is compatible with:
| Python 2.7, 3.3, 3.4, 3.5, 3.6
| Django 1.7, 1.8, 1.9
| Django REST Framework 2.5, 3.0, 3.1, 3.2, 3.3 (maybe 3.5+, but untested)

| Version 0.8 is compatible with:
| Python 2.7, 3.3, 3.4, 3.5, 3.6
| Django 1.10, 1.11
| Django REST Framework 3.6, 3.7

Documentation
-------------

Full documentation available at `Read the Docs <http://django-textplusstuff.readthedocs.org/en/latest/>`_.
