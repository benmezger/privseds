from django.urls import path, include

from .api import urls

app_name = "manager"
urlpatterns = [path("api/", include(urls))]

