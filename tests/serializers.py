from __future__ import unicode_literals

from rest_framework import serializers

from textplusstuff.serializers import (
    ExtraContextSerializerMixIn,
    TextPlusStuffFieldSerializer
)

from .models import RegisteredModel, TPSTestModel


class RegisteredModelSerializer(ExtraContextSerializerMixIn,
                                serializers.ModelSerializer):

    class Meta:
        model = RegisteredModel
        fields = ('title',)


class TPSTestModelSerializer(serializers.ModelSerializer):
    content = TextPlusStuffFieldSerializer()

    class Meta:
        model = TPSTestModel
        fields = ('content',)
