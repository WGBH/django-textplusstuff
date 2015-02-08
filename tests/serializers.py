from __future__ import unicode_literals

from rest_framework import serializers

from .models import RegisteredModel


class RegisteredModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisteredModel
        fields = ('title',)
