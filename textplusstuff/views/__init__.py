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
    pass


class RetrieveStuffView(TextPlusStuffAPIViewMixIn,
                        TextPlusStuffViewNameMixIn,
                        TextPlusStuffRetrieveModelMixin,
                        RetrieveAPIView):
    renditions = []
