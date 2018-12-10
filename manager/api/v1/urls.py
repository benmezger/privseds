from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from manager.api.v1.views import (
    EmailContentApiViewSet,
    InjectedEmailViewSet,
    EmailCategoryViewSet,
)

injected_list = InjectedEmailViewSet.as_view({"get": "list"})

urlpatterns = [
    path(
        "email-content/<int:pk>/",
        EmailContentApiViewSet.as_view(),
        name="email-content",
    ),
    path("injected-email/", injected_list, name="injected-email"),
    path(
        "email-category/<int:pk>/",
        EmailCategoryViewSet.as_view(),
        name="email-category",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
