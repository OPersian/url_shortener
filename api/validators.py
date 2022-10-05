"""
Custom validators for the url shortener API.
"""

from django.core.validators import URLValidator


class OptionalSchemeURLValidator(URLValidator):
    """
    Make URL protocol optional.
    """

    def __call__(self, value):
        if '://' not in value:
            value = 'http://' + value
        super(OptionalSchemeURLValidator, self).__call__(value)
