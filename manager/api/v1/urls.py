from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from manager.api.v1.views import (
    EmailContentApiViewSet,
    InjectedEmailViewSet
)

injected_list = InjectedEmailViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path("email-content/<int:pk>/", EmailContentApiViewSet.as_view(), name='email-content-api'),
    path("injected-email/", injected_list, name='injected-email'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
