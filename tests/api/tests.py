"""
Test url shortener API views.
"""
import logging

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# Disable logging for tests
logging.disable(logging.CRITICAL)


class BaseApiTest(TestCase):
    """
    Base API testing logic.
    """

    url = None  # Define in every subclass

    def setUp(self):
        self.client = APIClient()

    def populate_client_request(self, client_ip, original_url):
        """
        Populate tests with a client request to shorten url.
        """
        url = "/shorten_url/"
        data = {"url": original_url}
        header = {"HTTP_X_FORWARDED_FOR": client_ip}
        _ = self.client.post(url, data=data, **header)


class ShortenedUrlsCountViewTest(BaseApiTest):
    """
    Test ShortenedUrlsCountView logic.
    """

    url = "/shortened_urls_count/"

    def setUp(self):
        super(ShortenedUrlsCountViewTest, self).setUp()
        self._set_client_ips()
        # Protocol presence doesn't matter here
        self.original_url_1 = "www.example-1.com"
        self.original_url_2 = "https://www.example-2.com"

    def _set_client_ips(self):
        self.john_ip = "0.0.0.1"
        self.alice_ip = "0.0.0.2"
        self.bob_ip = "0.0.0.3"

    def test_zero_count(self):
        """
        No one made any request.

        Expected output: 0
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 0)

    def test_regular_case(self):
        """
        John made a request to shorten "www.example_1.com",
        Alice also made a request to shorten "www.example_1.com",
        and Bob made a request to shorten "www.example_2.com".

        Expected output: 3
        """
        self.populate_client_request(client_ip=self.john_ip, original_url=self.original_url_1)
        self.populate_client_request(client_ip=self.alice_ip, original_url=self.original_url_1)
        self.populate_client_request(client_ip=self.bob_ip, original_url=self.original_url_2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 3)

    def test_client_spammed_single_unique_original_url(self):
        """
        John made a request to shorten "www.example_1.com",
        Alice also made a request to shorten "www.example_1.com",
        and Bob made 5 requests from the same IP to shorten "www.example_2.com".

        Expected output: 3
        """
        self.populate_client_request(client_ip=self.john_ip, original_url=self.original_url_1)  # NOQA
        self.populate_client_request(client_ip=self.alice_ip, original_url=self.original_url_1)
        for _ in range(5):
            self.populate_client_request(client_ip=self.bob_ip, original_url=self.original_url_2)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 3)

    def test_client_spammed_several_unique_original_urls(self):
        """
        John made a request to shorten "www.example_1.com",
        Alice also made a request to shorten "www.example_1.com",
        and Bob made 5 requests from the same IP to shorten "www.example_1.com" and "www.example_2.com".

        Expected output: 4
        """
        self.populate_client_request(client_ip=self.john_ip, original_url=self.original_url_1)  # NOQA
        self.populate_client_request(client_ip=self.alice_ip, original_url=self.original_url_1)
        for _ in range(5):
            self.populate_client_request(client_ip=self.bob_ip, original_url=self.original_url_1)
            self.populate_client_request(client_ip=self.bob_ip, original_url=self.original_url_2)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 4)


class MostPopularShortenedUrlsViewTest(BaseApiTest):
    """
    Test MostPopularShortenedUrlsView logic.
    """
    url = "/most_popular_urls/"

    # TODO test: only 10 to show up!


# TODO ShortenUrlViewTest; both urls, w/ or w/o protocol, work fine!
# TODO FetchContentViewTest

