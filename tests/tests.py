from __future__ import unicode_literals
from collections import OrderedDict

from six.moves import reload_module

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core import serializers
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.utils import six

from rest_framework import __version__ as rest_framework_version
from rest_framework.renderers import JSONRenderer

from textplusstuff.datastructures import TextPlusStuff
from textplusstuff.exceptions import (
    AlreadyRegistered,
    AlreadyRegisteredRendition,
    ImproperlyConfiguredStuff,
    InvalidRenderOption,
    InvalidRendition,
    InvalidRenditionType,
    MalformedToken,
    MissingRendition,
    NonExistentGroup,
    NotRegistered
)
from textplusstuff.models import TextPlusStuffLink
from textplusstuff.parser.lexer import TextPlusStuffLexer
from textplusstuff.parser.nodes import (
    BaseNode, MarkdownFlavoredTextNode, ModelStuffNode
)
from textplusstuff.registry import stuff_registry, Rendition, ModelStuff
from textplusstuff.serializers import TextPlusStuffFieldSerializer

from .models import TPSTestModel, RegisteredModel
from .serializers import TPSTestModelSerializer, RegisteredModelSerializer


import logging

logging.basicConfig(filename='/tmp/rapi.log', level='INFO')

rest_framework_version = [
    int(seg)
    for seg in rest_framework_version.split('.')
]


class TextPlusStuffTestCase(TestCase):
    """The test suite for django-textplusstuff"""

    fixtures = ['textplusstuff.json']
    maxDiff = None

    def setUp(self):
        password = '12345'
        user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        client = Client()
        login = client.login(
            username='test',
            password=password
        )
        self.assertTrue(login)
        self.user = user
        self.client = client
        self.tps_test_instance = TPSTestModel.objects.get(pk=1)
        self.registered_model_instance = RegisteredModel.objects.get(pk=1)

    def test_admin(self):
        """
        Testing textplusstuff.admin.TextPlusStuffRegisteredModelAdmin
        token table response and textplusstuff.fields.TextPlusStuffField's
        formfield.
        """
        admin_path = '/admin/tests/registeredmodel/1/change/'

        response = self.client.get(admin_path)
        if six.PY2:
            response_content = response.content
        else:
            response_content = str(response.content, encoding='utf8')
        self.assertInHTML(
            """
<table>
    <tr>
        <th>Name</th>
        <th>Description</th>
        <th>Token</th>
    </tr>

    <tr>
        <td>Test Rendition</td>
        <td>Displays a Test Rendition rendered.</td>
        <td>{% textplusstuff &#39;MODELSTUFF__tests:registeredmodel:1:test_rendition&#39; %}</td>
    </tr>
</table>
            """,
            response_content
        )
        response = self.client.get(
            '/admin/tests/tpstestmodel/add/'
        )
        if six.PY2:
            response_content = response.content
        else:
            response_content = str(response.content, encoding='utf8')
        self.assertInHTML(
            '<textarea class="vLargeTextField textplusstuff" cols="40" '
            'id="id_content" name="content" rows="10" required>',
            response_content
        )
        tps_admin_path = '/admin/tests/tpstestmodel/1/change/'
        response = self.client.get(tps_admin_path)
        if six.PY2:
            response_content = response.content
        else:
            response_content = str(response.content, encoding='utf8')
        self.assertInHTML(
            '<textarea class="vLargeTextField textplusstuff" cols="40" '
            'id="id_content" name="content" rows="10" required>'
            '# I&#39;m an H1\n\n## I&#39;m an H2\n\n###I&#39;m an H3\n\n'
            'I&#39;m in a paragraph with **bold text** and _italic text_.\n\n'
            'And [a link](http://www.djangoproject.com), too!\n\n'
            '{% textplusstuff &#39;MODELSTUFF__tests:registeredmodel'
            ':1:test_rendition&#39; %}</textarea>',
            response_content
        )

    def test_api_stuffgroup_list_response(self):
        """Tests the TextPlusStuff API's 'ListStuffGroups' response"""
        response = self.client.get('/textplusstuff/')
        if six.PY2:
            response_content = response.content
        else:
            response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(
            response_content,
            [
                {
                    "stuff": [
                        {
                            "renditions": [
                                {
                                    "type": "block",
                                    "name": "Test Rendition",
                                    "short_name": "test_rendition",
                                    "description": (
                                        "Displays a Test Rendition rendered."
                                    )
                                }
                            ],
                            "instance_list": "http://testserver/textplusstuff/"
                                             "tests/registeredmodel/list/",
                            "name": "Registered Model",
                            "description": "Add an Registration Test Model"
                        }
                    ],
                    "name": "Testing!",
                    "short_name": "test_group",
                    "description": "For your test models!"
                }
            ]
        )

    def test_api_list_response(self):
        """Tests the TextPlusStuff API's 'ListStuffView' response"""
        response = self.client.get(
            '/textplusstuff/tests/registeredmodel/list/?format=json'
        )
        if six.PY2:
            response_content = response.content
        else:
            response_content = str(response.content, encoding='utf8')

        if rest_framework_version[0] >= 3 and rest_framework_version[1] >= 2:
            response_url = (
                'http://testserver/textplusstuff/tests/'
                'registeredmodel/detail/1/?format=json'
            )
        else:
            response_url = (
                'http://testserver/textplusstuff/tests/'
                'registeredmodel/detail/1/'
            )

        self.assertJSONEqual(
            response_content,
            [{
                'url': response_url,
                'id': 1,
                'title': 'Test Title'
            }]
        )

    def test_api_detail_response(self):
        """Tests the TextPlusStuff API's 'RetrieveStuffView' response"""
        response = self.client.get(
            '/textplusstuff/tests/registeredmodel/detail/1/'
        )
        if six.PY2:
            response_content = response.content
        else:
            response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(
            response_content,
            {
                'renditions': {
                    'test_rendition': {
                        'verbose_name': 'Test Rendition',
                        'token': "{% textplusstuff 'MODELSTUFF__tests"
                                 ":registeredmodel:1:test_rendition' %}",
                        'path_to_template': 'RegisteredModel_test_'
                                            'rendition.html',
                        'description': 'Displays a Test Rendition rendered.',
                        'type': 'block'
                    }
                },
                'context': {'title': 'Test Title', 'extra_context': {}}
            }
        )

    def test_api_as_html_description(self):
        response = self.client.get(
            '/textplusstuff/tests/registeredmodel/detail/1/?format=api'
        )
        if six.PY2:
            response_content = response.content
        else:
            response_content = str(response.content, encoding='utf8')
        self.assertIn(
            '<h1>Retrieve Registered Model Stuff</h1>',
            response_content
        )

    def test_textplusstufffield_responses(self):
        """
        Tests that the textplusstuff.fields.TextPlusStuffField's various
        responses come back as expected.
        """
        self.assertEqual(
            self.tps_test_instance.content.as_plaintext(),
            (
                "I'm an H1\nI'm an H2\nI'm an H3\nI'm in a paragraph "
                "with bold text and italic text.\nAnd a link, too!\n"
            )
        )
        self.assertEqual(
            self.tps_test_instance.content.as_markdown(),
            """# I'm an H1

## I'm an H2

###I'm an H3

I'm in a paragraph with **bold text** and _italic text_.

And [a link](http://www.djangoproject.com), too!"""
        )
        self.assertEqual(
            self.tps_test_instance.content.as_html(),
            (
                '<h1>I\'m an H1</h1>\n\n<h2>I\'m an H2</h2>\n\n'
                '<h3>I\'m an H3</h3>\n\n<p>I\'m in a paragraph with '
                '<strong>bold text</strong> and <em>italic text</em>.</p>\n\n'
                '<p>And <a href="http://www.djangoproject.com">a link</a>, '
                'too!</p>\n<h1>Test Title</h1>\n'
            )
        )
        self.assertEqual(
            self.tps_test_instance.content.as_html(
                include_content_nodes=False
            ),
            (
                '<h1>I\'m an H1</h1>\n\n<h2>I\'m an H2</h2>\n\n'
                '<h3>I\'m an H3</h3>\n\n<p>I\'m in a paragraph with '
                '<strong>bold text</strong> and <em>italic text</em>.</p>\n\n'
                '<p>And <a href="http://www.djangoproject.com">a link</a>, '
                'too!</p>\n'
            )
        )
        json_output = self.tps_test_instance.content.as_json(
            convert_to_json_string=True
        )
        self.assertJSONEqual(
            json_output,
            {
                "text_as_html": (
                    "<h1>I'm an H1</h1>\n\n<h2>I'm an H2</h2>\n\n"
                    "<h3>I'm an H3</h3>\n\n<p>I'm in a paragraph with "
                    "<strong>bold text</strong> and <em>italic text</em>.</p>"
                    "\n\n<p>And <a href=\"http://www.djangoproject.com\">a "
                    "link</a>, too!</p>\n<span data-textplusstuff-contentnode-"
                    "arrayindex=\"0\"></span>"
                ),
                "text_as_markdown": (
                    "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3\n\nI'm in a "
                    "paragraph with **bold text** and _italic text_.\n\nAnd "
                    "[a link](http://www.djangoproject.com), too!"
                    "{{ NODE__0 }}"
                ),
                "content_nodes": [
                    {
                        "model": "tests:registeredmodel",
                        "rendition": "test_rendition",
                        "context": {
                            "title": "Test Title",
                            "extra_context": {}
                        }
                    }
                ]
            }
        )

    def test_textplusstuff_invalid_initialization(self):
        """
        Ensures textplusstuff.datastructures.TextPlusStuff only accepts
        instances of basestring (and its subclasses).
        """
        with self.assertRaises(UnicodeError):
            TextPlusStuff({'foo': 'bar'})

    def test_TextPlusStuffLink_signals(self):
        """
        Ensures TextPlusStuffLink instances are created and deleted as
        expected.
        """
        x = __import__('tests')
        reload_module(x.stuff)
        x = TextPlusStuffLink.objects.get()
        self.assertEqual(
            x.parent_content_object,
            self.tps_test_instance
        )
        self.assertEqual(
            x.content_object,
            self.registered_model_instance
        )
        self.assertEqual(
            x.__str__(),
            'tpstestmodel:1 -> registeredmodel:1'
        )
        y = TextPlusStuffLink.objects.create(
            parent_content_type=x.parent_content_type,
            parent_object_id=2,
            content_type=x.content_type,
            object_id=2,
            field='foo'
        )
        y.save()
        self.assertEqual(
            y.__str__(),
            '<DoesNotExist> -> <DoesNotExist>'
        )
        new_instance_content = (
            "{% textplusstuff 'MODELSTUFF__tests:registeredmodel:"
            "1:test_rendition' %}"
        )
        new_instance = TPSTestModel(
            content=new_instance_content
        )
        tpstestmodel_ct = ContentType.objects.get_for_model(TPSTestModel)
        registered_model_ct = ContentType.objects.get_for_model(
            self.registered_model_instance.__class__
        )
        lookup_kwargs = {
            'parent_content_type': tpstestmodel_ct,
            'parent_object_id': 2,
            'content_type': registered_model_ct,
            'object_id': self.registered_model_instance.pk,
            'field': 'content'
        }
        with self.assertRaises(TextPlusStuffLink.DoesNotExist):
            x = TextPlusStuffLink.objects.get(
                **lookup_kwargs
            )
        new_instance.save()
        x = TextPlusStuffLink.objects.get(
            **lookup_kwargs
        )
        new_instance.content = ''
        new_instance.save()
        with self.assertRaises(TextPlusStuffLink.DoesNotExist):
            x = TextPlusStuffLink.objects.get(
                **lookup_kwargs
            )
        new_instance.content = new_instance_content
        new_instance.save()
        x = TextPlusStuffLink.objects.get(
            **lookup_kwargs
        )
        new_instance.delete()
        with self.assertRaises(TextPlusStuffLink.DoesNotExist):
            x = TextPlusStuffLink.objects.get(
                **lookup_kwargs
            )

    def test_MalformedToken_exception(self):
        """
        Ensures MalformedTokens are appropriately caught.
        """
        with self.assertRaises(MalformedToken):
            self.tps_test_instance.content = (
                "{% textplusstuff 'tests:registeredmodel:1:test_rendition' %}"
            )
            self.tps_test_instance.save()

    def test_nodes(self):
        """
        Tests code found within the textplusstuff.parser.nodes module
        """
        with self.assertRaises(NotImplementedError):
            class NewNode(BaseNode):
                pass
            x = NewNode('Test string')
            x.render()

        mftn = self.tps_test_instance.content.nodelist[0]
        self.assertTrue(
            isinstance(mftn, MarkdownFlavoredTextNode)
        )
        self.assertEqual(
            mftn.__repr__(),
            "<MarkdownFlavoredTextNode: '# I'm an H1## I'm an H2'>"
        )
        msn = self.tps_test_instance.content.nodelist[1]
        self.assertTrue(
            isinstance(msn, ModelStuffNode)
        )
        self.assertEqual(
            msn.__repr__(),
            "<ModelStuffNode: 'tests:registeredmodel:1:test_rendition'>"
        )
        with self.assertRaises(InvalidRenderOption):
            mftn.render('latex')

        invalid_modelstuffnode = ModelStuffNode(
            payload='missingapp:missingmodel:1:test_rendition'
        )

        with self.assertRaises(ObjectDoesNotExist):
            invalid_modelstuffnode.render()

        unregistered_modelstuffnode = ModelStuffNode(
            payload='tests:tpstestmodel:1:test_rendition'
        )

        with self.assertRaises(NotRegistered):
            unregistered_modelstuffnode.render()

        unavailable_instance_modelstuffnode = ModelStuffNode(
            payload='tests:registeredmodel:2:test_rendition'
        )

        with self.assertRaises(ObjectDoesNotExist):
            unavailable_instance_modelstuffnode.render()

        unavailable_rendition_modelstuffnode = ModelStuffNode(
            payload='tests:registeredmodel:1:unavailable_rendition'
        )

        with self.assertRaises(MissingRendition):
            unavailable_rendition_modelstuffnode.render()

    def test_tokens(self):
        """
        Tests that tokens print helpful human-readable representations
        in the shell.
        """
        lexer = TextPlusStuffLexer(self.tps_test_instance.content.raw_text)
        self.assertEqual(
            lexer.tokenize()[0].__str__(),
            """<MARKDOWNTEXT token: "# I'm an H...">"""
        )

    def test_InvalidRenditionType(self):
        """
        Tests the InvalidRenditionType exception
        """
        with self.assertRaises(InvalidRenditionType):
            class RegisteredModelStuff(ModelStuff):
                queryset = RegisteredModel.objects.all()
                description = 'Add an Registration Test Model'
                serializer_class = RegisteredModelSerializer
                renditions = [
                    Rendition(
                        short_name='foo',
                        verbose_name='Foo Rendition',
                        description='Displays a Foo Rendition rendered.',
                        path_to_template='nonexistant.html',
                        rendition_type='invalid_rendition_type'
                    )
                ]
                list_display = ('id', 'title')

            stuff_registry.add_modelstuff(
                RegisteredModel,
                RegisteredModelStuff,
                groups=['test_group']
            )

    def test_InvalidRendition(self):
        """
        Tests the InvalidRendition exception
        """
        with self.assertRaises(InvalidRendition):
            class RegisteredModelStuff(ModelStuff):
                queryset = RegisteredModel.objects.all()
                description = 'Add an Registration Test Model'
                serializer_class = RegisteredModelSerializer
                renditions = [
                    object()
                ]
                list_display = ('id', 'title')

            stuff_registry.add_modelstuff(
                RegisteredModel,
                RegisteredModelStuff,
                groups=['test_group']
            )

    def test_InvalidRendition_nonunique(self):
        """
        Tests the InvalidRendition exception when multiple renditions on the
        same stuff have the same short_name value
        """
        with self.assertRaises(InvalidRendition):
            class RegisteredModelStuff(ModelStuff):
                queryset = RegisteredModel.objects.all()
                description = 'Add an Registration Test Model'
                serializer_class = RegisteredModelSerializer
                renditions = [
                    Rendition(
                        short_name='foo',
                        verbose_name='Foo Rendition',
                        description='Displays a Foo Rendition rendered.',
                        path_to_template='nonexistant.html',
                        rendition_type='block'
                    ),
                    Rendition(
                        short_name='foo',
                        verbose_name='Foo Rendition Duplicate',
                        description='Displays a Foo Rendition rendered.',
                        path_to_template='nonexistant-duplicate.html',
                        rendition_type='block'
                    )
                ]
                list_display = ('id', 'title')

            stuff_registry.add_modelstuff(
                RegisteredModel,
                RegisteredModelStuff,
                groups=['test_group']
            )

    def test_ImproperlyConfiguredStuff_missing_renditions(self):
        """
        Tests the InvalidRendition exception when multiple renditions on the
        same stuff have the same short_name value
        """
        with self.assertRaises(ImproperlyConfiguredStuff):
            stuff_registry._registry = {}

            class RegisteredModelStuff(ModelStuff):
                queryset = RegisteredModel.objects.all()
                description = 'Add an Registration Test Model'
                serializer_class = RegisteredModelSerializer
                renditions = []
                list_display = ('id', 'title')

            stuff_registry.add_modelstuff(
                RegisteredModel,
                RegisteredModelStuff,
                groups=['test_group']
            )

    def test_NonExistentGroup(self):
        """
        Ensures the NonExistentGroup exception fires when appropriate
        """
        with self.assertRaises(NonExistentGroup):
            class RegisteredModelStuff(ModelStuff):
                queryset = RegisteredModel.objects.all()
                description = 'Add an Registration Test Model'
                serializer_class = RegisteredModelSerializer
                renditions = [
                    Rendition(
                        short_name='foo',
                        verbose_name='Foo Rendition',
                        description='Displays a Foo Rendition rendered.',
                        path_to_template='nonexistant.html',
                        rendition_type='block'
                    )
                ]
                list_display = ('id', 'title')

            stuff_registry.add_modelstuff(
                RegisteredModel,
                RegisteredModelStuff,
                groups=['non_existent_group']
            )

    def test_AlreadyRegistered(self):
        """
        Ensures the AlreadyRegistered exception fires when appropriate
        """
        with self.assertRaises(AlreadyRegistered):
            class DummyModelStuff(ModelStuff):
                renditions = [
                    Rendition(
                        short_name='foo',
                        verbose_name='foo',
                        description='foo',
                        path_to_template='foo.html')
                ]

            stuff_registry.add_modelstuff(
                RegisteredModel,
                DummyModelStuff,
                groups=['test_group']
            )

            stuff_registry.add_modelstuff(
                RegisteredModel,
                object,
                groups=['test_group']
            )

    def test_NotRegistered(self):
        """
        Ensures the NotRegistered exception fires when appropriate
        """
        with self.assertRaises(NotRegistered):
            stuff_registry.remove_modelstuff(RegisteredModel)

    @override_settings(
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.messages",
            "django.contrib.sessions",
            "django.contrib.staticfiles",
            "rest_framework",
            'textplusstuff',
        ),
        TEXTPLUSSTUFF_STUFFGROUPS=None
    )
    def test_missing_StuffGroups(self):
        """
        Raises ImproperlyConfigured if settings.TEXTPLUSSTUFF_STUFFGROUPS
        is unset.
        """
        with self.assertRaises(ImproperlyConfigured):
            response = self.client.get('/textplusstuff/')
            del response

    @override_settings(
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.messages",
            "django.contrib.sessions",
            "django.contrib.staticfiles",
            "rest_framework",
            'textplusstuff',
        ),
        TEXTPLUSSTUFF_STUFFGROUPS={'pickle': {'foo': 1, 'bar': 2}}
    )
    def test_improperly_structured_StuffGroup(self):
        """
        Raises ImproperlyConfigured if settings.TEXTPLUSSTUFF_STUFFGROUPS
        is set incorrectly.
        """
        with self.assertRaises(ImproperlyConfigured):
            response = self.client.get('/textplusstuff/')
            del response

    def test_TextPlusStuffSerializerField(self):
        """
        Ensures the TextPlusStuffFieldSerializer works as intended.
        """
        serializer = TPSTestModelSerializer(TPSTestModel.objects.get(pk=1))
        self.assertEqual(
            serializer.data,
            {'content': {
                'as_plaintext': "I'm an H1\nI'm an H2\nI'm an H3\nI'm in a "
                                "paragraph with bold text and italic text.\n"
                                "And a link, too!\n",
                'as_html': (
                    '<h1>I\'m an H1</h1>\n\n<h2>I\'m an H2</h2>\n\n<h3>I\'m '
                    'an H3</h3>\n\n<p>I\'m in a paragraph with <strong>bold '
                    'text</strong> and <em>italic text</em>.</p>\n\n<p>'
                    'And <a href="http://www.djangoproject.com">a link</a>, '
                    'too!</p>\n<h1>Test Title</h1>\n'
                ),
                'raw_text': "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3\n\n"
                            "I'm in a paragraph with **bold text** and "
                            "_italic text_.\n\nAnd [a link](http://www."
                            "djangoproject.com), too!\n\n{% textplusstuff "
                            "'MODELSTUFF__tests:registeredmodel:1:"
                            "test_rendition' %}",
                'as_html_no_tokens': (
                    '<h1>I\'m an H1</h1>\n\n<h2>I\'m an H2</h2>\n\n<h3>I\'m '
                    'an H3</h3>\n\n<p>I\'m in a paragraph with <strong>bold '
                    'text</strong> and <em>italic text</em>.</p>\n\n<p>And <a '
                    'href="http://www.djangoproject.com">a link</a>, '
                    'too!</p>\n'
                ),
                'as_markdown': "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3"
                               "\n\nI'm in a paragraph with **bold text** and "
                               "_italic text_.\n\nAnd [a link](http://www."
                               "djangoproject.com), too!",
                'as_json': {
                    "text_as_html": (
                        "<h1>I'm an H1</h1>\n\n<h2>I'm an H2</h2>\n\n<h3>I'm "
                        "an H3</h3>\n\n<p>I'm in a paragraph with <strong>"
                        "bold text</strong> and <em>italic text</em>.</p>\n\n"
                        "<p>And <a href=\"http://www.djangoproject.com\">a "
                        "link</a>, too!</p>\n<span data-textplusstuff-"
                        "contentnode-arrayindex=\"0\"></span>"
                    ),
                    "text_as_markdown": (
                        "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3\n\nI'm "
                        "in a paragraph with **bold text** and _italic text_."
                        "\n\nAnd [a link](http://www.djangoproject.com), "
                        "too!{{ NODE__0 }}"
                    ),
                    "content_nodes": [
                        {
                            "rendition": "test_rendition",
                            "model": "tests:registeredmodel",
                            "context": {
                                "title": "Test Title",
                                "extra_context": {}
                            }
                        }
                    ]
                }
            }}
        )
        with self.assertRaises(ValueError):
            # Ensuring only TextPlusStuffFields can be rendered by
            # TextPlusStuffFieldSerializer
            s = TextPlusStuffFieldSerializer()
            s.to_representation(value=self.registered_model_instance.title)

    def test_field_serialization(self):
        """
        Ensures TextPlusStuffField serializes correctly
        """
        output = serializers.serialize(
            'json',
            TPSTestModel.objects.filter(pk=1)
        )
        self.assertJSONEqual(
            output,
            [
                {
                    "fields": {
                        "content": (
                            "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3\n\n"
                            "I'm in a paragraph with **bold text** and "
                            "_italic text_.\n\nAnd "
                            "[a link](http://www.djangoproject.com), too!\n\n"
                            "{% textplusstuff 'MODELSTUFF__tests:"
                            "registeredmodel:1:test_rendition' %}"
                        ),
                        "content_constructed": "{}"
                    },
                    "model": "tests.tpstestmodel",
                    "pk": 1
                }
            ]
        )

    @override_settings(
        INSTALLED_APPS=(
            "rest_framework",
            'textplusstuff',
            'tests',
        )
    )
    def test_noncore_rendition_registration(self):
        """
        Test to see if 'non-core' Rendition registration works.
        """
        rendition = Rendition(
            short_name='baz',
            verbose_name='baz',
            description='baz',
            path_to_template='baz.html'
        )

        stuff_registry.add_noncore_modelstuff_rendition(
            RegisteredModel,
            rendition
        )

        self.assertTrue(
            2,
            len(
                stuff_registry._registry.get(
                    RegisteredModel
                )[0]._renditions
            )
        )
        self.assertNotEqual(
            None,
            stuff_registry._registry.get(
                RegisteredModel
            )[0]._renditions.get('baz', None)
        )

    @override_settings(
        INSTALLED_APPS=(
            "rest_framework",
            'textplusstuff',
            'tests',
        )
    )
    def test_add_dupe_noncore_rendition_registration(self):
        """
        Should raise AlreadyRegisteredRendition
        """
        with self.assertRaises(AlreadyRegisteredRendition):
            dupe_rendition = Rendition(
                short_name='test_rendition',
                verbose_name='Test Rendition',
                description='Displays a Test Rendition rendered.',
                path_to_template='RegisteredModel_test_rendition.html',
                rendition_type='block'
            )
            stuff_registry.add_noncore_modelstuff_rendition(
                RegisteredModel,
                dupe_rendition
            )

    @override_settings(
        INSTALLED_APPS=(
            "rest_framework",
            'textplusstuff',
        )
    )
    def test_noncore_rendition_registration_to_notregistered_model(self):
        """
        Should raise NotRegistered
        """
        with self.assertRaises(NotRegistered):
            from django.contrib.auth.models import User
            stuff_registry.add_noncore_modelstuff_rendition(
                User,
                Rendition(
                    short_name='bar',
                    verbose_name='Bar',
                    description='Bar Rendition',
                    path_to_template='bar.html',
                    rendition_type='block'
                )
            )

    def test_extra_context(self):
        """Tests the 'extra_context' functionality of .as_html()"""
        as_html_with_extra_context = self.tps_test_instance.content.as_html(
            extra_context={'foo': 'bar'}
        )
        self.assertInHTML(
            "<h2>bar</h2>",
            as_html_with_extra_context
        )

    def test_constructed_field(self):
        """Tests the 'constructed_field' functionality."""
        instance = self.tps_test_instance
        self.assertEqual(
            instance.content_constructed,
            OrderedDict()
        )
        instance.save()
        constructed_json = JSONRenderer().render(instance.content_constructed)
        if six.PY3:
            constructed_json = str(constructed_json, encoding='utf8')
        self.assertJSONEqual(
            constructed_json,
            {
                'as_plaintext': "I'm an H1\nI'm an H2\nI'm an H3\nI'm in a "
                                "paragraph with bold text and italic text.\n"
                                "And a link, too!\n",
                'as_html': (
                    '<h1>I\'m an H1</h1>\n\n<h2>I\'m an H2</h2>\n\n<h3>I\'m '
                    'an H3</h3>\n\n<p>I\'m in a paragraph with <strong>bold '
                    'text</strong> and <em>italic text</em>.</p>\n\n<p>'
                    'And <a href="http://www.djangoproject.com">a link</a>, '
                    'too!</p>\n<h1>Test Title</h1>\n'
                ),
                'raw_text': "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3\n\n"
                            "I'm in a paragraph with **bold text** and "
                            "_italic text_.\n\nAnd [a link](http://www."
                            "djangoproject.com), too!\n\n{% textplusstuff "
                            "'MODELSTUFF__tests:registeredmodel:1:"
                            "test_rendition' %}",
                'as_html_no_tokens': (
                    '<h1>I\'m an H1</h1>\n\n<h2>I\'m an H2</h2>\n\n<h3>I\'m '
                    'an H3</h3>\n\n<p>I\'m in a paragraph with <strong>bold '
                    'text</strong> and <em>italic text</em>.</p>\n\n<p>And <a '
                    'href="http://www.djangoproject.com">a link</a>, '
                    'too!</p>\n'
                ),
                'as_markdown': "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3"
                               "\n\nI'm in a paragraph with **bold text** and "
                               "_italic text_.\n\nAnd [a link](http://www."
                               "djangoproject.com), too!",
                'as_json': {
                    "text_as_html": (
                        "<h1>I'm an H1</h1>\n\n<h2>I'm an H2</h2>\n\n<h3>I'm "
                        "an H3</h3>\n\n<p>I'm in a paragraph with <strong>"
                        "bold text</strong> and <em>italic text</em>.</p>\n\n"
                        "<p>And <a href=\"http://www.djangoproject.com\">a "
                        "link</a>, too!</p>\n<span data-textplusstuff-"
                        "contentnode-arrayindex=\"0\"></span>"
                    ),
                    "text_as_markdown": (
                        "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3\n\nI'm "
                        "in a paragraph with **bold text** and _italic text_."
                        "\n\nAnd [a link](http://www.djangoproject.com), "
                        "too!{{ NODE__0 }}"
                    ),
                    "content_nodes": [
                        {
                            "rendition": "test_rendition",
                            "model": "tests:registeredmodel",
                            "context": {
                                "title": "Test Title",
                                "extra_context": {}
                            }
                        }
                    ]
                }
            }
        )
        original_title = self.registered_model_instance.title
        self.registered_model_instance.title = 'Test Title UPDATED'
        self.registered_model_instance.save()
        constructed_json_2 = JSONRenderer().render(
            TPSTestModel.objects.get(pk=1).content_constructed
        )
        if six.PY3:
            constructed_json_2 = str(constructed_json_2, encoding='utf8')
        self.assertJSONEqual(
            constructed_json_2,
            {
                'as_plaintext': "I'm an H1\nI'm an H2\nI'm an H3\nI'm in a "
                                "paragraph with bold text and italic text.\n"
                                "And a link, too!\n",
                'as_html': (
                    '<h1>I\'m an H1</h1>\n\n<h2>I\'m an H2</h2>\n\n<h3>I\'m '
                    'an H3</h3>\n\n<p>I\'m in a paragraph with <strong>bold '
                    'text</strong> and <em>italic text</em>.</p>\n\n<p>'
                    'And <a href="http://www.djangoproject.com">a link</a>, '
                    'too!</p>\n<h1>Test Title UPDATED</h1>\n'
                ),
                'raw_text': "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3\n\n"
                            "I'm in a paragraph with **bold text** and "
                            "_italic text_.\n\nAnd [a link](http://www."
                            "djangoproject.com), too!\n\n{% textplusstuff "
                            "'MODELSTUFF__tests:registeredmodel:1:"
                            "test_rendition' %}",
                'as_html_no_tokens': (
                    '<h1>I\'m an H1</h1>\n\n<h2>I\'m an H2</h2>\n\n<h3>I\'m '
                    'an H3</h3>\n\n<p>I\'m in a paragraph with <strong>bold '
                    'text</strong> and <em>italic text</em>.</p>\n\n<p>And <a '
                    'href="http://www.djangoproject.com">a link</a>, '
                    'too!</p>\n'
                ),
                'as_markdown': "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3"
                               "\n\nI'm in a paragraph with **bold text** and "
                               "_italic text_.\n\nAnd [a link](http://www."
                               "djangoproject.com), too!",
                'as_json': {
                    "text_as_html": (
                        "<h1>I'm an H1</h1>\n\n<h2>I'm an H2</h2>\n\n<h3>I'm "
                        "an H3</h3>\n\n<p>I'm in a paragraph with <strong>"
                        "bold text</strong> and <em>italic text</em>.</p>\n\n"
                        "<p>And <a href=\"http://www.djangoproject.com\">a "
                        "link</a>, too!</p>\n<span data-textplusstuff-"
                        "contentnode-arrayindex=\"0\"></span>"
                    ),
                    "text_as_markdown": (
                        "# I'm an H1\n\n## I'm an H2\n\n###I'm an H3\n\nI'm "
                        "in a paragraph with **bold text** and _italic text_."
                        "\n\nAnd [a link](http://www.djangoproject.com), "
                        "too!{{ NODE__0 }}"
                    ),
                    "content_nodes": [
                        {
                            "rendition": "test_rendition",
                            "model": "tests:registeredmodel",
                            "context": {
                                "title": "Test Title UPDATED",
                                "extra_context": {}
                            }
                        }
                    ]
                }
            }
        )
        self.registered_model_instance.title = original_title
        self.registered_model_instance.save()
