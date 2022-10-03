"""
Serializers for URL shortening API.
"""
from rest_framework import serializers

from shortening.models import Url


class ShortenedUrlSerializer(serializers.ModelSerializer):
    """
    Serializer for a `shortening.models.Url` model.
    """
    original_url = serializers.URLField(source="url")

    class Meta:
        model = Url
        fields = [
            "original_url",
        ]
