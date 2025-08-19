from common.utils.custom_response_decorator import custom_response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

from . import openapi_schema as schemas
from .models import CustomUser
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenVerifySerializer,
    SellerRegistrationSerializer,
    UserMeSerializer,
    UserUpdateSerializer,
)


@custom_response
class SellerRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SellerRegistrationSerializer

    @swagger_auto_schema(
        request_body=schemas.seller_registration_request,
        responses={201: schemas.seller_registration_response},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.to_representation(user), status=status.HTTP_201_CREATED)


@custom_response
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        request_body=schemas.login_request, responses={200: schemas.login_response}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer

    @swagger_auto_schema(
        request_body=schemas.token_verify_request, responses={200: schemas.token_verify_response}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMeSerializer

    @swagger_auto_schema(responses={200: schemas.me_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


@custom_response
class UserEditView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=schemas.edit_put_request, responses={200: schemas.edit_put_response}
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=schemas.edit_patch_request, responses={200: schemas.edit_patch_response}
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
