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


class RetrieveStuffView(TextPlusStuffAPIViewMixIn,
                        TextPlusStuffViewNameMixIn,
                        TextPlusStuffRetrieveModelMixin,
                        RetrieveAPIView):
    renditions = []
    model = None
