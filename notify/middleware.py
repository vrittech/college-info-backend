import threading

_request_local = threading.local()

class CaptureUserMiddleware:
    """
    Middleware to store the current request user.
    This allows signals to detect who performed the action.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_local.user = request.user if request.user.is_authenticated else None
        response = self.get_response(request)
        return response

def get_current_user():
    """
    Retrieve the user performing the request.
    Returns None if there's no user context.
    """
    return getattr(_request_local, "user", None)
