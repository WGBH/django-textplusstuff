from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import force_str

from BeautifulSoup import BeautifulSoup
from markdown2 import Markdown

from ..exceptions import InvalidToken, NotRegistered
from ..registry import stuff_registry


class BaseNode(object):
    """"""
    def __init__(self, payload):
        self.payload = payload


class MarkdownFlavoredTextNode(BaseNode):

    def __repr__(self):
        return force_str(
            "<MarkdownFlavoredTextNode: '%s'>" % self.payload[:25],
            'ascii',
            errors='replace'
        )

    def render(self, render_as='html'):
        """
        `render_as` can be one of three values:
            * 'html': Returns a block of markdown flavored text as HTML
            * 'plain_text': Returns a block of text with markdown syntax
                            removed
            * 'markdown': Returns the text as is.
        """
        if render_as in ['html', 'plain_text']:
            markdowner = Markdown()
            markdown_as_html = markdowner.convert(self.payload)
            if render_as == 'html':
                to_return = markdown_as_html
            else:
                to_return = ''.join(
                    BeautifulSoup(markdown_as_html).findAll(text=True)
                )
        elif render_as == 'markdown':
            to_return = self.payload
        else:
            raise Exception(
                "`render_as` must be either 'html', 'plain_text' or 'markdown'"
            )
        return to_return


class ModelStuffNode(BaseNode):
    """
    {% textplusstuff 'MODELSTUFF__{app_label}:{model}:{pk}:{rendition_key}:{field}' %}
    """
    node_args = (
        'content_type__app_label',
        'content_type__model',
        'object_id',
        'rendition_key',
        'field'
    )

    def __init__(self, payload):
        """
        `node_id`: A colon-separated string of positional arguments
                   that corresponds to self.node_args
                   Example Value:
                   'carousel:carousel:4:main:content'
        """
        super(ModelStuffNode, self).__init__(payload)
        node_mapping = self.get_node_mapping_by_payload(
            self.payload,
            *self.node_args
        )
        self.node_mapping = node_mapping

    @staticmethod
    def get_node_mapping_by_payload(payload, *node_args):
        # Split `node_id` in preparation for building `self.node_mapping`
        node_id_split = payload.split(':')

        # Initialize an empty dictionary
        node_mapping = {}
        # Iterate through each string in `node_id_split`...
        for index, node_segment in enumerate(node_id_split):
            try:
                # ...creating a key with a string from the same position
                # in `self.node_args` and a value `node_segment`
                node_mapping[node_args[index]] = node_segment
            except IndexError:
                # This exception will fire if we've already iterated through
                # every key in `self.node_args`. It can be safetly passed
                # since we wouldn't know how to deal with that value anyways.
                # This will allow any future subclasses to extend
                # `self.node_args` without having to rework this constructor.
                pass
        return node_mapping

    def __repr__(self):
        return force_str(
            "<ModelStuffNode: %s>" % self.payload,
            'ascii',
            errors='replace'
        )

    def get_contenttype(self):
        """
        Retrieves the content type instance associated with a
        node mapping.
        """
        app_label = self.node_mapping.get('content_type__app_label')
        model_as_str = self.node_mapping.get('content_type__model')
        try:
            ct = ContentType.objects.get(
                app_label=app_label,
                model=model_as_str
            )
        except ContentType.DoesNotExist:
            raise ContentType.DoesNotExist(
                "No ContentType instance could be retrieved with the "
                "app_label: {} and the model: {}.".format(
                    app_label, model_as_str
                )
            )
        else:
            return ct

    def get_model_class(self):
        """
        Returns the model class associated with self.node_mapping
        """
        ct = self.get_contenttype()
        return ct.model_class()

    def get_textplusstufflink_instance(self):
        from .models import TextPlusStuffLink
        try:
            ct = self.get_contenttype_by_node_mapping()
        except ObjectDoesNotExist:
            raise InvalidToken(
                "{} is an invalid (or broken) token since the ContentType "
                "associated with it could not be retrieved.".format(
                    self.payload
                )
            )
        else:
            try:
                node_content = TextPlusStuffLink.objects.get(
                    content_type=ct,
                    object_id=self.node_mapping.get('instance_pk'),
                    field=self.node_mapping.get('field', '')
                )
            except TextPlusStuffLink.DoesNotExist:
                node_content = None

            return node_content

    def render(self):
        """
        Transforms this node into HTML
        """
        # Step 1: Get Model associated with token
        model_cls = self.get_model_class()
        # Step 2: Find the model in stuff_registry._modelstuff_registry
        try:
            stuff_config, groups = stuff_registry._modelstuff_registry[model_cls]
        except KeyError:
            raise NotRegistered(
                "The model ({}) associated with this token (uid: {}) is not "
                "currently registered with "
                "textplusstuff.registry.stuff_registry and, therefore, could "
                "not be rendered.".format(model_cls, self.payload)
            )
        else:
            try:
                # Step 3: Use the associated Stuff queryset (and the
                #         token's ID) to retrieve the right instance.
                instance = stuff_config.queryset.get(
                    pk=self.node_mapping.get('object_id')
                )
            except stuff_config.queryset.model.DoesNotExist:
                raise stuff_config.queryset.model.DoesNotExist(
                    "The model instance associated with this token (uid: {}): "
                    "model: {}, pk: {} could not be retrieved and, therefore, "
                    "could not be rendered.".format(
                        self.payload,
                        model_cls,
                        self.node_mapping.get('object_id')
                    )
                )
            else:
                # Step 4: Grab the rendition instance associated with the token
                #         and combine its template with the context provided by
                #         the serializer.
                rendition = next(
                    r
                    for r in stuff_config.renditions
                    if r.short_name == self.node_mapping.get('rendition_key')
                )
                template = get_template(rendition.path_to_template)
                context = Context({
                    'context': stuff_config.serializer_class(instance).data,
                })
                # Step 5: Then return it bruh.
                return template.render(context)

__all__ = ('MarkdownFlavoredTextNode', 'ModelStuffNode')
