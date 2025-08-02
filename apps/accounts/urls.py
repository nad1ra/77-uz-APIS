from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import SellerRegistrationView, PhoneNumberTokenObtainPairView

urlpatterns = [
    path("seller/registration/", SellerRegistrationView.as_view(), name="seller-registration"),
    path("login/", PhoneNumberTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
