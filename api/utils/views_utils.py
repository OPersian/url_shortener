"""
Utilities for api views.
"""

from django.shortcuts import redirect


def redirect_adapted(url):
    """
    Adapter function for page redirection.

    This wrapper is handy for testing and future functionality extensions.

    NOTE: consider forwarding gracefully, i.e. checking if the website exists before forwarding.
    """
    return redirect(url)
