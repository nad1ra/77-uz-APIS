from common.utils.custom_response_decorator import custom_response
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from .models import CustomUser
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenVerifySerializer,
    CustomTokenRefreshSerializer,
    SellerRegistrationSerializer,
    UserMeSerializer,
    UserUpdateSerializer,
)


@extend_schema(
    tags=["Accounts"],
    description="Foydalanuvchini ro‘yxatdan o‘tkazish",
    request=SellerRegistrationSerializer,
    responses={201: SellerRegistrationSerializer},
)
@custom_response
class SellerRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SellerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.to_representation(user), status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Accounts"],
    description="Foydalanuvchi login (JWT token olish)",
    request=CustomTokenObtainPairSerializer,
    responses={200: CustomTokenObtainPairSerializer},
)
@custom_response
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Accounts"],
    description="JWT tokenni yangilash (refresh)",
    request=CustomTokenRefreshSerializer,
    responses={200: CustomTokenRefreshSerializer},
)
@custom_response
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer



@extend_schema(
    tags=["Accounts"],
    description="JWT tokenni tekshirish",
    request=CustomTokenVerifySerializer,
    responses={200: CustomTokenVerifySerializer},
)
@custom_response
class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer


@extend_schema(
    tags=["Accounts"],
    description="Hozirgi foydalanuvchi haqida ma'lumot olish",
    responses={200: UserMeSerializer},
)
@custom_response
class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMeSerializer

    def get_object(self):
        return self.request.user


@extend_schema(
    tags=["Accounts"],
    description="Hozirgi foydalanuvchi ma'lumotini yangilash",
    request=UserUpdateSerializer,
    responses={200: UserUpdateSerializer},
)
@custom_response
class UserEditView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
