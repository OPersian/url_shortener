"""
URL shortening utilities.
"""

import secrets
import string
from typing import Optional
from urllib.parse import urlunsplit

from django.conf import settings

from shortening.constants import KEY_LENGTH


def create_random_key(length: int = KEY_LENGTH) -> str:
    """
    Create a random key of a specified length.

    Example: "KLO7K9VV".
    """
    # TODO not all uppercase e.g. "ouoYFY48"
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


# TODO PEP params alignment
def create_shortened_url(key: str,
                         path: str = settings.NETLOC,
                         protocol: str = settings.SCHEME,
                         ) -> str:
    """
    Create a shortened url from given URL parts.
    """
    return urlunsplit((protocol, path, key, "", ""))
