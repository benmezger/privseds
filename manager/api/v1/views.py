from django.conf import settings
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from manager.models import EmailContent, InjectedEmailContent, EmailCategory
from manager.serializers import (
    EmailContentSerializer,
    InjectedEmailContentSerializer,
    EmailCategorySerializer,
)


class EmailContentApiViewSet(RetrieveUpdateDestroyAPIView):
    """
    List, create or update a new email content
    """

    queryset = EmailContent.objects.all()
    serializer_class = EmailContentSerializer


class InjectedEmailViewSet(ReadOnlyModelViewSet):
    queryset = InjectedEmailContent.objects.all()
    serializer_class = InjectedEmailContentSerializer


class EmailCategoryViewSet(RetrieveUpdateDestroyAPIView):
    queryset = EmailCategory.objects.all()
    serializer_class = EmailCategorySerializer
