# django-textplusstuff

## About

### Summary

A django-compatible field that makes it easy to intersperse 'stuff' into large (or small or anything-in-between) blocks of Markdown-flavored text.

### A Flexible Interface

`django-textplusstuff` provides a simple interface for returning the contents of your field however you like: as either markdown-flavored text, valid HTML markup (with or without 'stuff' interspersed) or even plain text (with all markdown formatting removed).

### Keep Track of Your Content

`django-textplusstuff` also keeps track of which model instances are associated within each TextPlusStuffField (via the `TextPlusStuffLink` model) so you can see where all your textplusstuff-integrated content is used across your django project.

### Easy Integration

Coming soon!

Registering existing models for use in TextPlusStuffFields is as easy as integrating a model into the admin.

### Designer/Front-End Developer Friendly

Coming soon!

Each model registered with `django-textplusstuff` can have as many 'renditions' as you like which keeps business logic DRY while enabling designers and front-end developers to have control over how content is displayed.

### Current Version ###

Alpha

## Requirements ##

* `django` >= 1.5
* `django-rest-framework` == 2.3.13
* `markdown2` >= 2.1.0
* `BeautifulSoup` >= 3.2.1

## Installation Instructions

_*NOTE:* The instructions below are for alpha development purposes and assume you already have a virtual environment setup with `virtualenvwrapper`. Once this thing is in PyPi it'll be a whole lot simpler._

1. Pull down this repo:

        $ git clone http://url.to/django-textplusstuff.git

2. Add the folder pointing to the newly cloned repo to your virtual environment:

        $ workon VirtualEnvName
        $ add2virtualenv path/to/django-textplusstuff.git

3. Install dependencies:

        $ pip install markdown2>= 2.1.0 BeautifulSoup>=3.2.1 djangorestframework==2.3

4. Add required settings:

    Add `textplusstuff` to `INSTALLED_APPS`:

        INSTALLED_APPS = (
            # Other apps here
            'rest_framework',
            'textplusstuff',
        )

    Add the TEXTPLUSSTUFF_STUFFGROUPS setting with at least one StuffGroup. It can be named whatever you like (the one below is just 'example'):

        TEXTPLUSSTUFF_STUFFGROUPS = {
            'example': {
                'name': 'Example',
                'description': "This is an example of a StuffGroup!"
            },
        }

    _*NOTE:* StuffGroups are used to organize Stuff in the upcoming editor tool and are required when you register Stuff._

5. Add textplusstuff-required bits to your project's base `urls.py`:

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

## Using textplusstuff

### Registering Stuff

To start using textplusstuff you have to register a model as Stuff. The examples below will use the creatively named `TestModel` which has one attribute, 'name' a `CharField`:

1. Create a file called `serializers.py` within the app that has the model you want to register as stuff:

        someproject/
            someapp/
                models.py
                serializers.py # Like this!

2. Now open `serializers.py` to create your first serializer. For more information on serializing models [check out django REST frameworks fantastic docs](http://www.django-rest-framework.org/api-guide/serializers#modelserializer).:

        # serializers.py

        from rest_framework.serializers import ModelSerializer

        from .models import TestModel

        class TestModelSerializer(ModelSerializer):

            class Meta:
                model = TestModel
                fields = (
                    'name',
                )

3. OK, now that we've got a serializer when need to create a file called `stuff.py` within the app that has the model you want to register as Stuff:

        someproject/
            someapp/
                models.py
                serializers.py
                stuff.py # Like this!

4. Now open the `stuff.py` file you just created and import the model you want to register and the serializer you just created:

        # someapp/stuff.py
        from textplusstuff import registry

        from .models import TestModel
        from .serializers import TestModelSerializer

        class TestModelStuff(registry.ModelStuff):
            # The queryset used to retrieve instances of TestModel
            # within the front-end interface. For instance, you could
            # exclude 'unpublished' instances or anything else you can
            # query the ORM against
            queryset = RoadshowTable.objects.all()

            # What humans see when they see this stuff
            verbose_name = 'Test Model'
            verbose_name_plural = 'Test Models'
            description = 'Add a Test Model'

            # The serializer we just defined, this is what provides the context/JSON
            # payload for this Stuff
            serializer_class = TestModelSerializer

            # All Stuff must have at least one rendition (specified in
            # the `renditions` attribute below) which basically
            # just points to a template and some human-readable metadata.
            # At present there are only two options for setting rendition_type:
            # either 'block' (the default) or inline. These will be used by
            # the front-end editor when placing tokens.
            renditions = [
                registry.Rendition(
                    short_name='sidebar_left',
                    verbose_name='Test Model Sidebar',
                    description='Displays a Test Model in the sidebar.',
                    path_to_template='someapp/templates/sidebar_left.html',
                    rendition_type='block'
                )
            ]
            # The attributes used in the list (table) display of the front-end
            # editing tool.
            list_display = ('id', 'name')

        # OK, now let's register our Model and its Stuff config:
        registry.stuff_registry.add_modelstuff(
            TestModel,
            TestModelStuff,
            groups=['image', 'media']
        )

    Once you've registered your Stuff you can test if it worked by firing up a webserver and visiting http://localhost:8000/textplusstuff/.

### Using the TextPlusStuff field:

Using a TextPlusStuff field is easy just import it and set it to an attribute. Any options available to a django TextField (like blank=True) can be set on a TextPlusStuffField:

    # someapp/models.py

    from django.db import models

    from textplusstuff.fields import TextPlusStuffField

    class MyModel(models.Model):
        content = TextPlusStuffField()

TextPlusStuff fields store rich text as markdown and can serve it back as either raw markdown, plain text (formatting removed), or as HTML (markdown entities converted into HTML tags):

    >>> from someapp.models import MyModel
    >>> instance = MyModel(content='Oh _hello there_!')
    >>> instance.save()
    >>> instance.content.as_markdown
    'Oh _hello there_!'
    >>> instance.content.as_plaintext
    'Oh hello there!'
    >>> instance.content.as_html
    'Oh <em>hello there</em>!'

Try pasting some tokens (that you find at /textplusstuff) into a TextPlusStuffField, saving the model instance associated with the field and then call the attributes above to see what happens. At present when a field with tokens is rendeered by `as_html` it will just transform the token in a generic way (to show that the field found/can-process it) but, once I get some time to come back to this the TextPlusStuff field will combine a template referenced in a Rendition with the context provided by its associated serializer and turn it into DOM.
