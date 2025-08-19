from rest_framework import serializers
from .models import Category, Ad, AdPhoto, FavouriteProduct
from accounts.models import CustomUser


class ChildCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.URLField()


class CategoryWithChildrenSerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True, source='child')  # `child` modeldagi related_name bo'lishi kerak

    class Meta:
        model = Category
        fields = ["id", "name", "icon", "children"]


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "icon", "product_count"]

    def get_product_count(self, obj):
        try:
            return obj.ads.count()
        except AttributeError:
            return 0


class SellerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "phone_number", "profile_photo"]


class AdPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdPhoto
        fields = ["id", "image", "is_main", "created_at"]


class AdCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)

    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    main_photo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    seller = SellerShortSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "name_uz",
            "name_ru",
            "description",
            "description_uz",
            "description_ru",
            "slug",
            "category",
            "price",
            "photos",
            "main_photo",
            "published_at",
            "address",
            "seller",
            "is_liked",
            "updated_time",
        ]
        extra_kwargs = {
            "name_uz": {"write_only": True},
            "name_ru": {"write_only": True},
            "description_uz": {"write_only": True},
            "description_ru": {"write_only": True},
            "category": {"write_only": True},
        }
        read_only_fields = [
            "id",
            "name",
            "slug",
            "main_photo",
            "published_at",
            "address",
            "seller",
            "is_liked",
            "updated_time",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        photos_data = validated_data.pop("photos", [])

        ad = Ad.objects.create(seller=user, **validated_data)

        if user and getattr(user, "address", None):
            ad.address = user.address
            ad.save()

        AdPhoto.objects.bulk_create([AdPhoto(ad=ad, image=img) for img in photos_data])

        return ad

    def get_name(self, obj):
        lang = getattr(self.context["request"], "LANGUAGE_CODE", "uz")
        return getattr(obj, f"name_{lang}", obj.name_uz)

    def get_description(self, obj):
        lang = getattr(self.context["request"], "LANGUAGE_CODE", "uz")
        return getattr(obj, f"description_{lang}", obj.description_uz)

    def get_main_photo(self, obj):
        first_photo = obj.photos.first()
        return first_photo.image.url if first_photo else None

    def get_address(self, obj):
        return obj.seller.address.name if getattr(obj.seller, "address", None) else None

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user if request else None
        if user and user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data.get("description"):
            data.pop("description")
        return data


class AdDetailSerializer(serializers.ModelSerializer):
    photos = AdPhotoSerializer(many=True, read_only=True)
    seller = SellerShortSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "description",
            "price",
            "photos",
            "published_at",
            "seller",
            "is_liked",
            "view_count",
            "updated_time",
        ]

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user if request else None
        if user and user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False


class FavouriteProductSerializer(serializers.ModelSerializer):
    product = AdDetailSerializer(read_only=True)

    class Meta:
        model = FavouriteProduct
        fields = ["id", "user", "device_id", "product", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        device_id = attrs.get("device_id")

        if not user.is_authenticated and not device_id:
            raise serializers.ValidationError(
                "Anonymous users must provide a device_id."
            )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user if self.context["request"].user.is_authenticated else None
        device_id = validated_data.get("device_id")
        product = validated_data["product"]

        if user:
            obj, _ = FavouriteProduct.objects.get_or_create(user=user, product=product)
        else:
            obj, _ = FavouriteProduct.objects.get_or_create(device_id=device_id, product=product)

        return obj
