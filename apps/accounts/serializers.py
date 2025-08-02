from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser, Address


class CustomUserSerializer(serializers.ModelSerializer):
    address = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = [
            "full_name",
            "project_name",
            "phone_number",
            "email",
            "category",
            "address",
            "status"
        ]
        extra_kwargs = {
            "email": {"required": False},
            "status": {"read_only": True},
        }

    def create(self, validated_data):
        address_name = validated_data.pop("address", None)
        address = Address.objects.create(name=address_name) if address_name else None
        validated_data["address"] = address
        return CustomUser.objects.create(**validated_data)


class PhoneNumberTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "phone_number"

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if user.status != "approved":
            raise serializers.ValidationError(
                {"error": "Hali admin tomonidan tasdiqlanmadingiz."}
            )

        return data
