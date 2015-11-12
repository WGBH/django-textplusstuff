.. django-textplusstuff documentation master file, created by
   sphinx-quickstart on Mon Feb  9 09:12:04 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================================
Welcome to django-textplusstuff's documentation!
================================================

.. image:: https://travis-ci.org/WGBH/django-textplusstuff.svg?branch=master
    :target: https://travis-ci.org/WGBH/django-textplusstuff
    :alt: Travis CI Status

.. image:: https://img.shields.io/coveralls/WGBH/django-textplusstuff.svg?style=flat
    :target: https://coveralls.io/r/WGBH/django-textplusstuff
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/dm/django-textplusstuff.svg?style=flat
    :target: https://pypi.python.org/pypi/django-textplusstuff/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/django-textplusstuff.svg?style=flat
    :target: https://pypi.python.org/pypi/django-textplusstuff/
    :alt: Latest Version

----

About
=====

Summary
-------

A django field that makes it easy to intersperse 'stuff' into blocks of text.

Documentation
-------------

Full documentation available at `Read the Docs <http://django-textplusstuff.readthedocs.org/en/latest/>`_.

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

Current Version
---------------

0.4.1

Dependencies
------------

- ``markdown2`` >= 2.3.x
- ``beautifulsoup4`` >= 4.3.1
- ``django`` >= 1.6.x
- ``djangorestframework`` >= 2.4.4

Python Compatibility
````````````````````

-  2.7.x
-  3.3.x
-  3.4.x

Django Compatibility
````````````````````

-  1.6.x
-  1.7.x
-  1.8.x

Django REST Framework Compatibility
```````````````````````````````````

-  2.4.4
-  3.0.x
-  3.1.x
-  3.2.x
-  3.3.x (**NOTE:** Django 1.6.x is not compatible with DRF 3.3.x)

Contents
========

.. toctree::
   :maxdepth: 4

   installation
   using_textplusstuff
   drf_integration
   improving_performance

Release Notes
=============

0.4.1
-----

- Fixed a UnicodeDecodeError bug that arose in Python 2.7.5 when encoding text nodes that had non-ASCII encoded HTML entities.

0.4
---

- Added :ref:`ExtraContextSerializerMixin <extra-context-serializer-mixin>` for simplifying ``extra_context``-to-serializer handoff.

0.3
---

- Added the ability to :ref:`register 'non-core' renditions <non-core-renditions>` in a third-party application's already-registered Stuff class.
- ``django-textplusstuff`` is now available for installation via `wheel <http://wheel.readthedocs.org/en/latest/>`_.

0.2.1
-----

- Squashed a bug that prevented ``TextPlusStuffField`` from serializing correctly (when using ``dumpdata``).

0.2
---

-  Added Django REST Framework :doc:`serialization </drf_integration>` for ``TextPlusStuffField``

0.1.3
-----

-  Fixed a Python 2.7.x-related encoding issue in the Stuff registry.

0.1.2
-----

-  Another ``pip`` installation hotfix: including template files in distribution.

0.1.1
-----

-  Squashed ``pip`` installation bug

0.1
---

-  Initial open source release

Roadmap to v1.0
===============

-  Create a javascript powered editor for writing markdown-flavored text and placing tokens.
-  textplusstuff API POST support (so model instances registered with the stuff_registry can be created directly from a TextPlusStuff field widget)
-  Document 'Constructed Field' functionality to improve performance.
-  Document 'as_json' method on a TextPlusStuff instance.


