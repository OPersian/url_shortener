"""
Views logic of the URL Shortener API.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import HandleAPIExceptionMixin
from api.serializers import ShortenedUrlSerializer
from shortening.models import ClientIp, OriginalUrl, ShortenedUrlData, UrlShorteningRequest
from shortening.utils.url_shortening_utils import create_shortened_url
from shortening.utils.client_data_utils import get_client_ip

# TODO introduce logging


class FetchContentView(HandleAPIExceptionMixin, APIView):
    """
    Fetch original content via a shortened url.

    URL: `/<str:key>/`

    GET response example (status 200): TODO TBD
    GET response example (status 404): TODO TBD key not found
    GET response example (status 400): TODO TBD
    """

    def get(self, request, *args, **kwargs):
        # TODO if a get request is made to the shortened url then the user should be redirected to the the original url,
        #  or returned the contents of the original url.

        #  TODO Graceful Forward: Check if the website exists before forwarding.
        key = kwargs.get("key")
        url = ShortenedUrlData.objects.filter(key=key).first()
        if url:
            # TODO redirect / return content
            return Response({'heyya': url.original_url.url}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "TBD error msg"}, status=status.HTTP_404_NOT_FOUND)


# TODO rewrite as generic
class ShortenUrlView(HandleAPIExceptionMixin, APIView):
    """
    Logic to shorten a provided url or provide its content.

    URL: `/shorten_url/`

    POST parameters example:
        {
            "url": "www.helloworld.com"
        }

    POST response example (status 201):
        {
            "shortened_url": 'http://www.your_service.com/ouoYFY48'
        }

    POST response example (status 400). Use case: inappropriate original URL format provided:
       {
            "url": [
                "Enter a valid URL."
            ]
        }
    """

    serializer_class = ShortenedUrlSerializer
    # queryset = Url.objects.all()

    def post(self, request, format=None):
        original_url = self.request.data.get("url")
        key = ShortenedUrlData.create_unique_random_key()
        shortened_url = create_shortened_url(key=key)
        server_serializer = ShortenedUrlSerializer(data={
            "url": original_url,
        })
        if server_serializer.is_valid():
            original_url_obj = OriginalUrl.objects.create(url=original_url)
            shortened_url_data = ShortenedUrlData.objects.create(original_url=original_url_obj, key=key)

            client_ip, created = ClientIp.objects.get_or_create(client_ip=get_client_ip(request))
            _ = UrlShorteningRequest.objects.create(
                client_ip=client_ip,
                url=original_url_obj,
                key=shortened_url_data,
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

    TODO NOTE: If Bob makes 20 requests from the same IP to shorten the same url,
    then the number of shortened urls count should only increase by one,
    i.e. the count increases by the number of unique urls provided from the same IP.

    TODO NOTE: return zero (0) if no requests were made / no urls were shortened (btw is it the same?..):

    GET response example (status 200): integer value
        3
    """


class MostPopularShortenedUrlsView(HandleAPIExceptionMixin, generics.ListAPIView):
    """
    Return a list of the 10 most shortened urls.

    NOTE: could be an empty list, if no requests were made to shorten an url.

    GET response example (status 200). Use case: if John made a request to shorten www.google.com,
        Alice also made a request to shorten www.google.com, and Bob made a request to shorten www.amazon.com:
            [
                "www.google.com",
                "www.amazon.com"
            ]
    """
