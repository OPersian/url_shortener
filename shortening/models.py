"""
URL shortener shortening layer.
"""
from django.db import models

from shortening.constants import KEY_LENGTH


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
    """

    original_url = models.URLField(unique=True)
    shortened_url_key = models.CharField(unique=True, max_length=KEY_LENGTH, null=True)

    class Meta:
        db_table = "url"

    def __str__(self):
        return f"{self.__name__} original: {self.original_url}"


class UserIp(CommonInfo):
    """
    IP a user made a request from (IPv4).
    """
    # TODO validate 0.0. 0.0 to 255.255.255.255
    # TODO can it be NULL?
    user_ip = models.CharField(max_length=15, null=True)

    class Meta:
        db_table = "user_ip"

    def __str__(self):
        return f"{self.__name__} : {self.user_ip}"


class UrlShorteningRequest(CommonInfo):
    """
    All URL-unique requests users ever made to shorten provided URLs.
    """
    user_ip = models.ForeignKey(UserIp, on_delete=models.RESTRICT)
    url = models.ForeignKey(Url, on_delete=models.RESTRICT)

    class Meta:
        db_table = "url_shortening_request"

    def __str__(self):
        return f"{self.__name__} : {self.pk}"
