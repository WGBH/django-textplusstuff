from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .datastructures import RichText
from .fields import RichTextField
from .parser import RichTextContentNode

@receiver(post_save)
def construct_RichTextLink_attachments(sender, instance, **kwargs):
    """
    Creates/Updates/Deletes RichTextLink instances for any `instance`
    that has one or more RichTextField fields.
    """

    richtext_fields = [
        field.name
        for field in instance._meta.fields
        if field.__class__ is RichTextField
    ]
    if richtext_fields:
        from .models import RichTextLink
        parent_ct = ContentType.objects.get_for_model(instance.__class__)
        for field in richtext_fields:
            # First, find any previously created RichTextLink instances
            # attached to this field on this particular instance
            previously_attached_instances = [
                richtextlink_instance
                for richtextlink_instance in RichTextLink.objects.filter(
                    parent_content_type=parent_ct,
                    parent_object_id=instance.pk,
                    field=field
                ).select_related('parent_content_type', 'content_type')
            ]

            # Next, pull the content assigned to the RichTextField field and...
            current_richtextfield_val = getattr(instance, field)
            # ...ensure that it is a RichText instance
            if not isinstance(current_richtextfield_val, RichText):
                # If not, convert it to RichText
                richtext_instance = RichText(raw_text=current_richtextfield_val)
            else:
                richtext_instance = current_richtextfield_val

            # Now, build a list of all RichTextContentNode
            # instances associated with it
            richtextlink_nodes = [
                node
                for node in richtext_instance.nodelist
                if isinstance(node, RichTextContentNode)
            ]

            # Now, iterate through each node...
            for node in richtextlink_nodes:
                # ...to get its node_mapping so...
                node_mapping = node.node_mapping
                # You can get its child ContentType instance and...
                ct = ContentType.objects.get_by_natural_key(
                    app_label=node_mapping.get('content_type__app_label'),
                    model=node_mapping.get('content_type__model'),
                )
                # ...build out a set of kwargs used for...
                get_or_create_kwargs = {
                    'content_type':ct,
                    'object_id':node_mapping.get('object_id'),
                    'field':field,
                    'parent_content_type':parent_ct,
                    'parent_object_id':instance.pk,
                }
                # ...either creating or retrieving a RichTextLink instance
                richtextlink_instance, created = RichTextLink.objects.get_or_create(
                    **get_or_create_kwargs
                )
                # Finally...
                try:
                    # Remove the RichTextLink instance you just got/created
                    # from `previously_attached_instances`
                    previously_attached_instances.remove(richtextlink_instance)
                except ValueError:
                    # Unless it wasn't in there to begin with (which is fine)
                    pass

            # Any instances that weren't removed in the above forloop are now 'orphans'
            # and can be safetly deleted.
            for previously_attached_instance in previously_attached_instances:
                previously_attached_instance.delete()
    return

@receiver(post_delete)
def delete_attached_RichTextLink_instances(sender, instance, **kwargs):
    """
    Deletes any RichTextLink instances attached to `instance` after
    `instance` is deleted.
    """
    richtext_fields = [
        field.name
        for field in instance._meta.fields
        if field.__class__ is RichTextField
    ]
    if richtext_fields:
        from .models import RichTextLink
        instance_ct = ContentType.objects.get_for_model(instance.__class__)
        attached_richtextlink_instances = RichTextLink.objects.filter(
            parent_content_type=instance_ct,
            parent_object_id=instance.pk
        )
        attached_richtextlink_instances.delete()
    return

