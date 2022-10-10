"""
Serializers for URL shortening API.
"""
from rest_framework import serializers


class OriginalUrlDataListSerializer(serializers.ListSerializer):  # NOQA
    """
    List serializer for a `shortening.models.OriginalUrlDataList`.
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
        return [obj.url for obj in data]


class OriginalUrlDataSerializer(serializers.Serializer):  # NOQA
    """
    Serializer for a `shortening.models.OriginalUrl` model.
    """
    url = serializers.URLField()

    class Meta:
        list_serializer_class = OriginalUrlDataListSerializer
        fields = [
            "url",
        ]
