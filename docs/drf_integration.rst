Django REST Framework Integration
=================================

If you've got an API powered by `Tom Christie <https://twitter.com/_tomchristie>`_'s excellent `Django REST Framework <http://www.django-rest-framework.org/>`_ you can serve the content of a ``TextPlusStuffField`` simultaneously in a variety of formats with the ``TextPlusStuffFieldSerializer``.

.. _example-model:

Example
-------

To demonstrate how it works we'll use this simple model:

.. code-block:: python

    # myproject/content/models.py

    from django.db import models

    from textplusstuff.fields import TextPlusStuffField


    class Content(models.Model):
        """Represents a person."""
        content = TextPlusStuffField('Content')

        class Meta:
            verbose_name = 'Content Block'
            verbose_name_plural = 'Content Blocks'

.. _serialization:

OK, let's write a simple ``ModelSerializer`` subclass to serialize Content instances:

.. code-block:: python
    :emphasize-lines: 5,12,17

    # myproject/content/serializers.py

    from rest_framework import serializers

    from textplusstuff.serializers import TextPlusStuffFieldSerializer

    from .models import Content


    class ContentSerializer(serializers.ModelSerializer):
        """Serializes Person instances"""
        content = TextPlusStuffFieldSerializer()

        class Meta:
            model = Content
            fields = (
                'content',
            )

And here's what it would look like serialized:

.. code-block:: python
    :emphasize-lines: 11-15

    >>> from myproject.content.models import Content
    >>> content = Person.objects.create(
    ...     content="""# Oh hello!\n\nHere's some _italic_ and **bold** text."""
    ... )
    >>> content.save()
    >>> from myproject.content.serializers import ContentSerializer
    >>> content_serialized = ContentSerializer(content)
    >>> content_serialized.data
    {
        'content': {
            'raw_text': "# Oh hello!\n\nHere's some _italic_ and **bold** text.", # The 'raw' content of the field as it is stored in the database.
            'as_plaintext': "Oh hello!\n\nHere's some italic and bold text.", # The content of this field as plaintext (all markup/formatting and tokens removed)
            'as_markdown': "# Oh hello!\n\nHere's some _italic_ and **bold** text.", # The content of this field as markdown (with tokens removed)
            'as_html': "<h1>Oh hello!</h1>\n\n<p>Here's some <em>italic</em> and <strong>bold</strong> text.", # The content of this field as HTML with tokens rendered
            'as_html_no_tokens': "<h1>Oh hello!</h1>\n\n<p>Here's some <em>italic</em> and <strong>bold</strong> text.", # The content of this field as HTML with tokens removed
        }
    }

.. note:: The example content used above doesn't include any tokens which is why the ``'as_html'`` and ``'as_html_no_tokens'`` as well as the ``'raw_text'`` and ``'as_markdown'`` values are identical.
