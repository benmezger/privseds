from django.conf import settings
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from manager.models import EmailContent, InjectedEmailContent
from manager.serializers import EmailContentSerializer, InjectedEmailContentSerializer


class EmailContentApiViewSet(RetrieveUpdateDestroyAPIView):
    """
    List, create or update a new email content
    """

    queryset = EmailContent.objects.all()
    serializer_class = EmailContentSerializer


class InjectedEmailViewSet(ReadOnlyModelViewSet):
    queryset = InjectedEmailContent.objects.all()
    serializer_class = InjectedEmailContentSerializer


# Create your views here.
