"""
Factories for REST API tests.
"""
import factory

from shortening.models import (
    ClientData,
    OriginalUrlData,
    ShortenedUrlData,
    UrlShorteningRequest,
)


class ClientDataFactory(factory.django.DjangoModelFactory):
    """
    ClientData model factory for tests.
    """

    client_ip = "0.0.0.0"

    class Meta:
        model = ClientData
        django_get_or_create = (
            "client_ip",
        )


class OriginalUrlDataFactory(factory.django.DjangoModelFactory):
    """
    OriginalUrlData model factory for tests.
    """

    url = 'http://example.com'
    unique_ip_hits = 0

    class Meta:
        model = OriginalUrlData
        django_get_or_create = (
            "url",
            "unique_ip_hits",
        )


class ShortenedUrlDataFactory(factory.django.DjangoModelFactory):
    """
    ShortenedUrlData model factory for tests.
    """

    key = "AAABBBB0"
    original_url_data = factory.SubFactory(OriginalUrlDataFactory)

    class Meta:
        model = ShortenedUrlData
        django_get_or_create = (
            "key",
            "original_url_data",
        )


class UrlShorteningRequestFactory(factory.django.DjangoModelFactory):
    """
    UrlShorteningRequest model factory for tests.
    """

    client_data = factory.SubFactory(ClientDataFactory)
    original_url_data = factory.SubFactory(OriginalUrlDataFactory)
    shortened_url_data = factory.SubFactory(ShortenedUrlDataFactory)

    class Meta:
        model = UrlShorteningRequest
        django_get_or_create = (
            "client_data",
            "original_url_data",
            "shortened_url_data",
        )
