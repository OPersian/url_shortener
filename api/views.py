"""
Views logic of the URL Shortener API.
"""
from django.db.models import Sum
from api.utils.views_utils import redirect_adapted
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import HandleAPIExceptionMixin
from api.serializers import OriginalUrlDataSerializer
from shortening.constants import ZERO
from shortening.models import ClientData, OriginalUrlData, ShortenedUrlData, UrlShorteningRequest
from shortening.utils.url_shortening_utils import create_shortened_url
from shortening.utils.client_data_utils import get_client_ip

# NOTE: introduce logging


class FetchContentView(HandleAPIExceptionMixin, APIView):
    """
    Fetch original content via a shortened url.

    URL: `/<str:key>/`

    GET response example (status 200): fetched content.

    GET response example (status 404):
        ```
        {"detail": "Shortened url with key 'OUOYFY48' is not found."}
        ```
    """

    def get(self, request, *args, **kwargs):
        key = kwargs.get("key")
        shortened_url_data = ShortenedUrlData.objects.filter(key=key).first()
        if shortened_url_data:
            url = shortened_url_data.original_url_data.url
            return redirect_adapted(url)
        else:
            return Response(
                {"detail": f"Shortened url with key '{key}' is not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class ShortenUrlView(HandleAPIExceptionMixin, APIView):
    """
    Logic to shorten a provided url or provide its content.

    URL: `/shorten_url/`

    POST parameters example:
        ```
        {
            "url": "www.helloworld.com"
        }
        ```

    POST response example (status 201):
        ```
        {
            "shortened_url": 'http://www.your_service.com/ouoYFY48'
        }
        ```

    POST response example (status 400). Use case: inappropriate original URL format provided:
       ```
       {
            "url": [
                "Enter a valid URL."
            ]
        }
       ```
    """

    def post(self, request, format=None):
        # NOTE: consider omitting trailing slash, for "https://google.com" and "https://google.com/"
        #  to be considered the same url.

        # NOTE: also, regardless of protocol, urls could be considered the same,
        #  e.g. "https://google.com" and "http://google.com"

        # NOTE: and now, both concerns combined: protocol and trailing slash; both to be considered the same:
        #  "https://google.com" and "http://google.com/"

        original_url = self.request.data.get("url")

        # NOTE: move it to the serializer (figure out a way to make validate() or validate_url() work).
        if '://' not in original_url:
            original_url = 'http://' + original_url

        key = ShortenedUrlData.create_unique_random_key()
        shortened_url = create_shortened_url(key=key)
        server_serializer = OriginalUrlDataSerializer(data={
            "url": original_url,
        })

        if server_serializer.is_valid():
            original_url_data, created_od = OriginalUrlData.objects.get_or_create(url=original_url)
            shortened_url_data = ShortenedUrlData.objects.create(original_url_data=original_url_data, key=key)

            client_ip = get_client_ip(request)
            client_data, created_cd = ClientData.objects.get_or_create(client_ip=client_ip)

            OriginalUrlData.increment_unique_ip_count(original_url, client_ip, original_url_data)

            _ = UrlShorteningRequest.objects.create(
                client_data=client_data,
                original_url_data=original_url_data,
                shortened_url_data=shortened_url_data,
            )

            return Response({'shortened_url': shortened_url}, status=status.HTTP_201_CREATED)
        else:
            return Response(server_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShortenedUrlsCountView(HandleAPIExceptionMixin, APIView):
    """
    Show how many urls have been shortened.

    Use case: if John made a request to shorten www.google.com,
    Alice also made a request to shorten www.google.com, and Bob made a request
    to shorten www.amazon.com, return an integer value 3.

    NOTE: If Bob makes 20 requests from the same IP to shorten the same url,
    then the number of shortened urls count should only increase by one,
    i.e. in this case, the count increases by the number of unique urls provided from Bob's IP.

    GET response example (status 200): integer value. NOTE: return zero (0) if no requests were made.
        ```
        3
        ```
    """

    def get(self, request, *args, **kwargs):
        count = OriginalUrlData.objects.aggregate(
            Sum("unique_ip_hits")
        ).get("unique_ip_hits__sum") or ZERO
        return Response(count, status=status.HTTP_200_OK)


class MostPopularUrlsView(HandleAPIExceptionMixin, generics.ListAPIView):
    """
    Return a list of the 10 most shortened urls.

    NOTE: could be an empty list, if no requests were made to shorten an url.

    GET response example (status 200). Use case: if John made a request to shorten www.google.com,
        Alice also made a request to shorten www.google.com,
        and Bob made a request to shorten www.amazon.com:
            ```
            [
                "www.google.com",
                "www.amazon.com"
            ]
            ```

    NOTE: Same prerequisite here. If Bob makes 20 requests from the same IP to shorten the same url,
    then the number of shortened urls count should only increase by one,
    i.e. in this case, the count increases by the number of unique urls provided from Bob's IP.
    """

    LIMIT = 10
    serializer_class = OriginalUrlDataSerializer
    queryset = OriginalUrlData.objects.all().order_by("-unique_ip_hits")[:LIMIT]
