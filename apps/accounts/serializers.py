from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import UntypedToken

from .models import CustomUser, Address, Category


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ["name", "lat", "long"]


class SellerRegistrationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )
    category_id = serializers.IntegerField(
        source="category.id",
        read_only=True
    )
    status = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "full_name",
            "project_name",
            "phone_number",
            "category",
            "category_id",
            "address",
            "status",
        ]

    def create(self, validated_data):
        address_data = validated_data.pop("address", None)  # 🔹 None bo‘lishi mumkin
        category = validated_data.pop("category")

        address = None
        if address_data:
            address = Address.objects.create(**address_data)

        user = CustomUser.objects.create(
            **validated_data,
            category=category,
            address=address,
            is_active=False,
            role=CustomUser.Role.SELLER,
            status=CustomUser.Status.PENDING
        )
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["address"] = instance.address.name if instance.address else None
        return data



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        user = authenticate(phone_number=phone_number, password=password)
        if not user or not user.is_active:
            raise AuthenticationFailed(
                "No active account found with the given credentials",
                code="authorization"
            )

        return super().validate(attrs)


class CustomTokenVerifySerializer(TokenVerifySerializer):
    token_class = UntypedToken

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["valid"] = True
        validated_data["user_id"] = getattr(self, "user", None).id if hasattr(self, "user") else None
        return validated_data


class UserMeSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "phone_number", "profile_photo", "address"]

    def get_profile_photo(self, obj):
        if obj.profile_photo and hasattr(obj.profile_photo, "url"):
            return obj.profile_photo.url
        return None


class UserUpdateSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
        required=False
    )
    profile_photo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["full_name", "phone_number", "profile_photo", "address"]
        read_only_fields = ["profile_photo"]

    def get_profile_photo(self, obj):
        if obj.profile_photo and hasattr(obj.profile_photo, "url"):
            return obj.profile_photo.url
        return None

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
