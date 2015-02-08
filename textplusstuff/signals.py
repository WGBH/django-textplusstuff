from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .fields import TextPlusStuffField
from .parser import ModelStuffNode


@receiver(post_save)
def construct_TextPlusStuffLink_attachments(sender, instance, **kwargs):
    """
    Creates/Updates/Deletes TextPlusStuffLink instances for any `instance`
    that has one or more TextPlusStuffField fields.
    """

    textplusstuff_fields = [
        field.name
        for field in instance._meta.fields
        if field.__class__ is TextPlusStuffField
    ]
    if textplusstuff_fields:
        from .models import TextPlusStuffLink
        parent_ct = ContentType.objects.get_for_model(instance.__class__)
        for field in textplusstuff_fields:
            # First, find any previously created TextPlusStuffLink instances
            # attached to this field on this particular instance
            previously_attached_instances = [
                textplusstufflink_instance
                for textplusstufflink_instance in TextPlusStuffLink.
                objects.filter(
                    parent_content_type=parent_ct,
                    parent_object_id=instance.pk,
                    field=field
                ).select_related('parent_content_type', 'content_type')
            ]

            # Next, pull the content assigned to the TextPlusStuffField field
            # and...
            current_textplusstufffield_val = getattr(instance, field)

            # Now, build a list of all ModelStuffNode
            # instances associated with it
            textplusstufflink_nodes = [
                node
                for node in current_textplusstufffield_val.nodelist
                if isinstance(node, ModelStuffNode)
            ]
            # Now, iterate through each node...
            for node in textplusstufflink_nodes:
                # ...to get its node_mapping so...
                node_mapping = node.node_mapping
                # You can get its child ContentType instance and...
                ct = ContentType.objects.get_by_natural_key(
                    app_label=node_mapping.get('content_type__app_label'),
                    model=node_mapping.get('content_type__model'),
                )
                # ...build out a set of kwargs used for...
                get_or_create_kwargs = {
                    'content_type': ct,
                    'object_id': node_mapping.get('object_id'),
                    'field': field,
                    'parent_content_type': parent_ct,
                    'parent_object_id': instance.id,
                }
                # ...either creating or retrieving a TextPlusStuffLink instance
                textplusstufflink_instance, created = TextPlusStuffLink.\
                    objects.get_or_create(
                        **get_or_create_kwargs
                    )
                # Finally...
                try:
                    # Remove the TextPlusStuffLink instance you just
                    # got/created from `previously_attached_instances`
                    previously_attached_instances.remove(
                        textplusstufflink_instance
                    )
                except ValueError:
                    # Unless it wasn't in there to begin with (which is fine)
                    pass

            # Any instances that weren't removed in the above forloop are now
            # 'orphans' and can be safetly deleted.
            for previously_attached_instance in previously_attached_instances:
                previously_attached_instance.delete()
    return


@receiver(post_delete)
def delete_attached_TextPlusStuffLink_instances(sender, instance, **kwargs):
    """
    Deletes any TextPlusStuffLink instances attached to `instance` after
    `instance` is deleted.
    """
    textplusstuff_fields = [
        field.name
        for field in instance._meta.fields
        if field.__class__ is TextPlusStuffField
    ]
    if textplusstuff_fields:
        from .models import TextPlusStuffLink
        instance_ct = ContentType.objects.get_for_model(instance.__class__)
        attached_textplusstufflink_instances = TextPlusStuffLink.\
            objects.filter(
                parent_content_type=instance_ct,
                parent_object_id=instance.pk
            )
        attached_textplusstufflink_instances.delete()
    return
