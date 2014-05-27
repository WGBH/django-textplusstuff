from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from .mixins import TextPlusStuffRetrieveModelMixin, \
    TextPlusStuffViewNameMixIn


class ListStuffView(TextPlusStuffViewNameMixIn,
                    ListAPIView):
    pass


class RetrieveStuffView(TextPlusStuffViewNameMixIn,
                        TextPlusStuffRetrieveModelMixin,
                        RetrieveAPIView):
    renditions = []
