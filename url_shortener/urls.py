"""
url_shortener URL Configuration
"""
from django.urls import path, include


urlpatterns = [
    path("", include("api.urls")),
]
