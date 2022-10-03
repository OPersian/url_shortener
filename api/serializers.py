"""
Serializers for URL shortening API.
"""
from rest_framework import serializers

from shortening.models import OriginalUrlData, ShortenedUrlData, UrlShorteningRequest


class OriginalUrlDataSerializer(serializers.ModelSerializer):
    """
    Serializer for a `shortening.models.OriginalUrl` model.
    """
    url = serializers.URLField()

    class Meta:
        model = OriginalUrlData
        fields = [
            "url",
        ]


class UrlShorteningRequestListSerializer(serializers.ListSerializer):
    """
    List serializer for a `shortening.models.UrlShorteningRequest`.
    """

    def to_representation(self, data):
        """
        List of object urls.

        Example of representation:
            [
                "www.google.com",
                "www.amazon.com"
            ]
        """
        return [obj.original_url_data.url for obj in data]


class UrlShorteningRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for a `shortening.models.UrlShorteningRequest` model.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = UrlShorteningRequest
        list_serializer_class = UrlShorteningRequestListSerializer
        fields = [
            "url",
        ]

    @staticmethod
    def get_url(obj):
        """
        Get an original url provided a shortened one.
        """
        return obj.original_url_data.url
