"""
Serializers for URL shortening API.
"""
from rest_framework import serializers

from api.validators import OptionalSchemeURLValidator
from shortening.models import OriginalUrlData


class OriginalUrlDataListSerializer(serializers.ListSerializer):
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


class OriginalUrlDataSerializer(serializers.ModelSerializer):
    """
    Serializer for a `shortening.models.OriginalUrl` model.
    """
    url = serializers.SerializerMethodField(validators=[OptionalSchemeURLValidator()])

    class Meta:
        model = OriginalUrlData
        list_serializer_class = OriginalUrlDataListSerializer
        fields = [
            "url",
        ]

    @staticmethod
    def get_url(obj):
        """
        Make URL protocol (schema) optional in the user input.

        Store the full path with schema though.
        """
        if '://' not in obj.url:
            # FIXME in the db, store with protocol
            # NOTE: consider secure protocols
            url = 'http://' + obj.url
            print(url)
        else:
            url = obj.url
        return url
