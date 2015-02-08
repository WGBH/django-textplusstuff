from __future__ import unicode_literals

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from .mixins import (
    TextPlusStuffRetrieveModelMixin,
    TextPlusStuffViewNameMixIn,
    TextPlusStuffAPIViewMixIn
)


class ListStuffView(TextPlusStuffAPIViewMixIn,
                    TextPlusStuffViewNameMixIn,
                    ListAPIView):
    model = None
    queryset = None


class RetrieveStuffView(TextPlusStuffAPIViewMixIn,
                        TextPlusStuffViewNameMixIn,
                        TextPlusStuffRetrieveModelMixin,
                        RetrieveAPIView):
    renditions = []
    model = None
