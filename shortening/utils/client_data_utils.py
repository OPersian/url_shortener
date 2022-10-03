"""
Utilities related to client data.
"""


# TODO consider security and other concerns
def get_client_ip(request):
    """
    Get client IP.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
