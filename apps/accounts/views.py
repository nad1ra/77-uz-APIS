from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, PhoneNumberTokenObtainPairSerializer


class SellerRegistrationView(APIView):

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Ariza yuborildi. Admin tasdiqlagach login va parol beriladi."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberTokenObtainPairView(TokenObtainPairView):
    serializer_class = PhoneNumberTokenObtainPairSerializer
