import threading

_request_user = threading.local()

class CaptureUserMiddleware:
    """
    Middleware to track the current request's user.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_user.value = request.user
        response = self.get_response(request)
        return response

def get_current_user():
    """
    Retrieve the request user.
    """
    return getattr(_request_user, "value", None)
