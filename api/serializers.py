"""
Serializers for URL shortening API.
"""
from rest_framework import serializers

from shortening.models import OriginalUrl


class ShortenedUrlSerializer(serializers.ModelSerializer):
    """
    Serializer for a `shortening.models.Url` model.
    """
    url = serializers.URLField()

    class Meta:
        model = OriginalUrl
        fields = [
            "url",
        ]
