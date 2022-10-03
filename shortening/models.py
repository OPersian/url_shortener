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


class OriginalUrlData(CommonInfo):
    """
    Original URL to be shortened.
    """

    # TODO consider indexing
    url = models.URLField()

    class Meta:
        db_table = "original_url_data"

    # FIXME fix this here and in other models
    # def __str__(self):
    #     return f"{self.__name__}: {self.pk}, {self.url}"


class ShortenedUrlData(CommonInfo):
    """
    Shortened URL data.

    A single original url can have multiple shortened url keys.
    """

    original_url_data = models.ForeignKey(OriginalUrlData, on_delete=models.RESTRICT)
    # TODO consider indexing
    key = models.CharField(unique=True, max_length=15)

    class Meta:
        db_table = "shortened_url_data"

    # def __str__(self):
    #     return f"{self.__name__}: {self.pk}, {self.key}"

    @staticmethod
    def create_unique_random_key(length: int = KEY_LENGTH) -> str:
        """
        Create a random key, ensuring its uniqueness.
        """
        key = create_random_key(length)
        while ShortenedUrlData.objects.filter(key=key).exists():
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

    # def __str__(self):
    #     return f"{self.__name__} : {self.client_ip}"


class UrlShorteningRequest(CommonInfo):
    """
    All requests clients ever made to shorten provided URLs.
    """

    client_ip = models.ForeignKey(ClientIp, on_delete=models.RESTRICT)
    original_url_data = models.ForeignKey(OriginalUrlData, on_delete=models.RESTRICT)
    shortened_url_data = models.ForeignKey(ShortenedUrlData, on_delete=models.RESTRICT)

    class Meta:
        db_table = "url_shortening_request"

    # def __str__(self):
    #     return f"{self.__name__} : {self.pk}"
