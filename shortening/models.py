"""
URL shortener shortening layer.
"""
from django.db import models

from shortening.constants import KEY_LENGTH
from shortening.utils.url_shortening_utils import create_random_key


# NOTE: consider putting indexes to url and url key


class CommonInfo(models.Model):
    """
    Common info for reuse by other shortening.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OriginalUrlData(CommonInfo):
    """
    Original URL to be shortened.
    """

    url = models.URLField(unique=True)
    unique_ip_hits = models.IntegerField(default=0)

    class Meta:
        db_table = "original_url_data"

    @staticmethod
    def increment_unique_ip_count(original_url, client_ip, original_url_data):
        """
        Increment unique-ip count for the original url.
        """
        if not UrlShorteningRequest.objects.filter(
            original_url_data__url=original_url,
            client_data__client_ip=client_ip,
        ).exists():
            current_unique_ip_hits_count = original_url_data.unique_ip_hits
            original_url_data.unique_ip_hits = current_unique_ip_hits_count + 1
            original_url_data.save()


class ShortenedUrlData(CommonInfo):
    """
    Shortened URL data.

    A single original url can have multiple shortened url keys.
    """

    key = models.CharField(unique=True, max_length=15)
    original_url_data = models.ForeignKey(OriginalUrlData, on_delete=models.RESTRICT)

    class Meta:
        db_table = "shortened_url_data"

    @staticmethod
    def create_unique_random_key(length: int = KEY_LENGTH) -> str:
        """
        Create a random key, ensuring its uniqueness.
        """
        key = create_random_key(length)
        while ShortenedUrlData.objects.filter(key=key).exists():
            key = create_random_key(length)
        return key


class ClientData(CommonInfo):
    """
    IP a client made a request from.
    """

    client_ip = models.GenericIPAddressField(unique=True, null=True)

    class Meta:
        db_table = "client_data"


class UrlShorteningRequest(CommonInfo):
    """
    All requests clients ever made to shorten provided URLs.
    """

    client_data = models.ForeignKey(ClientData, on_delete=models.RESTRICT)
    original_url_data = models.ForeignKey(OriginalUrlData, on_delete=models.RESTRICT)
    shortened_url_data = models.ForeignKey(ShortenedUrlData, on_delete=models.RESTRICT)

    class Meta:
        db_table = "url_shortening_request"
