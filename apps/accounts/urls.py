from django.urls import path

from . import views

urlpatterns = [
    path("seller/registration/", views.SellerRegistrationView.as_view(), name="register-seller"),
    path("login/", views.CustomLoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", views.CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", views.CustomTokenVerifyView.as_view(), name="token_verify"),
    path("me/", views.MeView.as_view(), name="account-me"),
    path("edit/", views.UserEditView.as_view(), name="account-edit"),
]
