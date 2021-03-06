from django.conf import settings
from rest_framework import serializers

from .models import InjectedEmailContent, EmailContent, EmailCategory


class InjectedEmailContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InjectedEmailContent
        fields = ("subject", "body")


class EmailContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailContent
        fields = ("subject", "body", "variables")


class EmailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCategory
        fields = ("name", "mailing_list", "created_date")
