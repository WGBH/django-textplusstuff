from __future__ import unicode_literals

from textplusstuff import registry
from django.contrib.auth.models import User

registry.stuff_registry.add_noncore_modelstuff_rendition(
    User,
    registry.Rendition(
        short_name='bar',
        verbose_name='Bar',
        description='Bar Rendition',
        path_to_template='bar.html',
        rendition_type='block'
    )
)
