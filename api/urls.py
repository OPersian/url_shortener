"""
URLs for the URL shortener API endpoints.
"""
from django.urls import path

from api import views


urlpatterns = [
    path(
        "shorten_url/",
        views.ShortenUrlView.as_view(),
        name="shorten-url",
    ),
    path(
        "shortened_urls_count/",
        views.ShortenedUrlsCountView.as_view(),
        name="shortened-urls-count",
    ),
    path(
        "most_popular_urls/",
        views.MostPopularUrlsView.as_view(),
        name="most-popular-urls",
    ),
    path(
        "<str:key>/",
        views.FetchContentView.as_view(),
        name="fetch-content",
    ),
]
