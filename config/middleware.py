# config/middleware.py

class APILanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bu yerga kerakli kod yozishingiz mumkin
        response = self.get_response(request)
        return response
