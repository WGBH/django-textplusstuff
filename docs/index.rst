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

.. image:: https://pypip.in/py_versions/django-textplusstuff/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-textplusstuff/
    :alt: Supported Python versions

.. image:: https://pypip.in/download/django-textplusstuff/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-textplusstuff/
    :alt: Downloads

.. image:: https://pypip.in/version/django-textplusstuff/badge.svg?style=flat
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

0.1

Dependencies
````````````

- ``django`` >= 1.6.x >
- ``djangorestframework`` >= 2.3.14
- ``markdown2`` >= 2.3.x
- ``beautifulsoup4`` >= 4.3.1

Contents
========

.. toctree::
   :maxdepth: 4

   installation
   using_textplusstuff

Release Notes
=============

0.1
---

-  Initial open source release

Roadmap to v1.0
===============

-  Create a javascript powered editor for writing markdown-flavored text and placing tokens.


