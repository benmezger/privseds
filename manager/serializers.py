from django.conf import settings
from rest_framework import serializers

from .models import InjectedEmailContent, EmailContent


class InjectedEmailContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InjectedEmailContent
        fields = ("subject", "body")


class EmailContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailContent
        fields = ("subject", "body", "variables")
