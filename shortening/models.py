"""
URL shortener shortening layer.
"""
from django.db import models

from shortening.constants import KEY_LENGTH
from shortening.utils.url_shortening_utils import create_random_key


class CommonInfo(models.Model):
    """
    Common info for reuse by other shortening.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Url(CommonInfo):
    """
    Pair of corresponding original URL and corresponding and shortened URL key.

    A single original url can have multiple shortened url keys.
    """

    # TODO consider indexing both fields
    original_url = models.URLField()
    # TODO consider moving out to a separate table
    shortened_url_key = models.CharField(unique=True, max_length=15)

    class Meta:
        db_table = "url"

    def __str__(self):
        return f"{self.__name__}: {self.pk}, {self.shortened_url_key}"

    @staticmethod
    def create_unique_random_key(length: int = KEY_LENGTH) -> str:
        """
        Create a random key, ensuring its uniqueness.
        """
        key = create_random_key(length)
        while Url.objects.filter(shortened_url_key=key).exists():
            key = create_random_key(length)
        return key


class ClientIp(CommonInfo):
    """
    IP a client made a request from (IPv4).
    """

    # TODO validate 0.0.0.0 to 255.255.255.255
    client_ip = models.CharField(unique=True, max_length=15, null=True)

    class Meta:
        db_table = "client_ip"

    def __str__(self):
        return f"{self.__name__} : {self.client_ip}"


class UrlShorteningRequest(CommonInfo):
    """
    All requests clients ever made to shorten provided URLs.
    """

    client_ip = models.ForeignKey(ClientIp, on_delete=models.RESTRICT)
    url = models.ForeignKey(Url, on_delete=models.RESTRICT)

    class Meta:
        db_table = "url_shortening_request"

    def __str__(self):
        return f"{self.__name__} : {self.pk}"
