"""
Test url shortener API views.
"""
import logging

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# Disable logging for tests
logging.disable(logging.CRITICAL)

NON_EXISTING_ENTRY_ID = 777


class BaseApiTest(TestCase):
    """
    Base API testing logic.
    """

    def setUp(self):
        self.client = APIClient()

    def populate_all(self):
        """
        Populate tests with all test data.
        """


# TODO FetchContentViewTest
# TODO ShortenUrlViewTest
# TODO ShortenedUrlsCountViewTest
# TODO MostPopularShortenedUrlsViewTest
