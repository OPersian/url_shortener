"""
Custom API exceptions.
"""
from rest_framework import status


class ApiCustomException(Exception):
    """
    Class for custom API exceptions.
    """

    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "An API exception occurred."

    def __init__(self, message=None, status_=None):
        """
        Initialization of an exceptions class object.
        """
        self.message = message or self.default_detail
        self.status = status_ or self.default_status_code
        super().__init__(message)

    def __str__(self):
        """
        Override string representation of an exceptions class object.
        """
        return self.message
