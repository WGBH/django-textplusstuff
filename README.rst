====================
django-textplusstuff
====================

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

Requirements
````````````

- ``django`` >= 1.6.x >
- ``djangorestframework`` >= 2.3.14
- ``markdown2`` >= 2.3.x
- ``beautifulsoup4`` >= 4.3.1