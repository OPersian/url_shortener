"""
Collection of useful mixins.
"""

from django.db.models.deletion import RestrictedError
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import ApiCustomException


class HandleAPIExceptionMixin(APIView):
    """
    Mixin to override handle_exception method in rest_framework views.

    Mix it in all API views for consistent exceptions handling.
    """

    def handle_exception(self, exc):
        """
        Handle custom exceptions.
        """
        if isinstance(exc, ApiCustomException):
            return Response(
                {
                    "detail": exc.message,
                },
                status=exc.status,
            )

        # Violation of `on_delete=models.RESTRICT` constraint.
        if isinstance(exc, RestrictedError):
            return Response(
                {
                    "detail": f"Cannot remove the record. {repr(exc)}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if isinstance(exc, IntegrityError):
            return Response(
                {
                    "detail": f"Integrity Error occurred. {repr(exc)}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().handle_exception(exc)
