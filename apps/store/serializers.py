from rest_framework import serializers
from accounts.models import CustomUser
from common.models import Region
from django.utils.text import slugify
from .models import Category, Ad, AdPhoto, FavouriteProduct, MySearch, SearchCount


class ChildCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.URLField()


class CategoryWithChildrenSerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True, source='child')

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
    product_id = serializers.IntegerField(write_only=True)
    product_id_read = serializers.IntegerField(source='ad.id', read_only=True)

    class Meta:
        model = AdPhoto
        fields = ["id", "image", "is_main", "product_id", "created_at", "product_id_read"]
        extra_kwargs = {
            "product_id": {"write_only": True}
        }

    def create(self, validated_data):
        product_id = validated_data.pop("product_id")

        try:
            ad = Ad.objects.get(id=product_id)
        except Ad.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Bunday product mavjud emas"})

        validated_data["ad"] = ad
        return AdPhoto.objects.create(**validated_data)



class AdListSerializer(serializers.ModelSerializer):
    seller = SellerShortSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    address = serializers.CharField(source='address.name', read_only=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "photo",
            "published_at",
            "address",
            "seller",
            "is_liked",
            "updated_time",
        ]

    def get_is_liked(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return FavouriteProduct.objects.filter(user=user, product=obj).exists()
        return False

    def get_photo(self, obj):
        first_photo = obj.photos.first()
        if first_photo:
            request = self.context.get("request")
            return request.build_absolute_uri(first_photo.image.url) if request else first_photo.image.url
        return None


class AdCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)

    name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
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
            "description_uz",
            "description_ru",
            "slug",
            "category",
            "price",
            "photos",
            "photo",
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
            "slug": {"read_only": True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        photos_data = validated_data.pop("photos", [])

        ad = Ad.objects.create(seller=user, **validated_data)

        lang = getattr(request, "LANGUAGE_CODE", "uz")
        name_value = getattr(ad, f"name_{lang}", ad.name)
        ad.slug = slugify(name_value)
        ad.save()

        if user and getattr(user, "address", None):
            ad.address = user.address
            ad.save()

        AdPhoto.objects.bulk_create([AdPhoto(ad=ad, image=img) for img in photos_data])

        return ad

    def get_name(self, obj):
        lang = getattr(self.context["request"], "LANGUAGE_CODE", "uz")
        return getattr(obj, f"name_{lang}", obj.name_uz)

    def get_photo(self, obj):
        first_photo = obj.photos.first()
        return first_photo.image.url if first_photo else None

    def get_address(self, obj):
        if obj.address:
            return obj.address.name
        return None

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user if request else None
        if user and user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AdDetailSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    seller = SellerShortSerializer(read_only=True)
    category = CategorySimpleSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    address = serializers.CharField(source='seller.address', read_only=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "photos",
            "published_at",
            "address",
            "seller",
            "category",
            "is_liked",
            "view_count",
            "updated_time",
        ]

    def get_photos(self, obj):
        return [photo.image.url for photo in obj.photos.all()]

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user if request else None
        if user and user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False


class FavouriteProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = FavouriteProduct
        fields = ["id", "product", "device_id", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        device_id = attrs.get("device_id")
        product = attrs.get("product")

        if not user.is_authenticated and not device_id:
            raise serializers.ValidationError("Anonymous foydalanuvchilar device_id kiritishi shart.")

        exists = FavouriteProduct.objects.filter(
            user=user if user.is_authenticated else None,
            device_id=device_id if not user.is_authenticated else None,
            product=product
        ).exists()

        if exists:
            raise serializers.ValidationError("Ushbu sevimli mahsulot allaqachon mavjud.")

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user if self.context["request"].user.is_authenticated else None
        device_id = validated_data.get("device_id")
        product = validated_data.get("product")

        if user:
            favourite, _ = FavouriteProduct.objects.get_or_create(user=user, product=product)
        else:
            favourite, _ = FavouriteProduct.objects.get_or_create(device_id=device_id, product=product)

        return favourite

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.user:
            rep.pop("device_id", None)
        return rep


class MyAdsListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    address = serializers.CharField(source='address.name', read_only=True)
    price = serializers.FloatField()

    class Meta:
        model = Ad
        fields = [
            'id', 'name', 'slug', 'price', 'photo',
            'published_at', 'address', 'status',
            'view_count', 'updated_time'
        ]

    def get_photo(self, obj):
        main_photo = obj.photos.filter(is_main=True).first()
        request = self.context.get('request')
        if main_photo:
            return request.build_absolute_uri(main_photo.image.url) if request else main_photo.image.url
        return None


class MyAdsDetailSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            'id', 'name', 'slug', 'description', 'category', 'price',
            'photos', 'published_at', 'status', 'view_count', 'updated_time'
        ]

    def get_photos(self, obj):
        request = self.context.get('request')
        photo_urls = [photo.image.url for photo in obj.photos.all()]
        if request:
            photo_urls = [request.build_absolute_uri(url) for url in photo_urls]
        return photo_urls


class FavouriteProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="product.id", read_only=True)
    name = serializers.CharField(source="product.name", read_only=True)
    slug = serializers.SlugField(source="product.slug", read_only=True)
    description = serializers.CharField(source="product.description", read_only=True)
    price = serializers.IntegerField(source="product.price", read_only=True)
    published_at = serializers.DateTimeField(source="product.published_at", read_only=True)

    address = serializers.CharField(source="product.address.name", read_only=True)
    seller = serializers.SerializerMethodField()

    photo = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    updated_time = serializers.DateTimeField(source="product.updated_time", read_only=True)

    def get_photo(self, obj):
        photo = obj.product.photos.first()
        return photo.image.url if photo else None

    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.product.likes.filter(id=user.id).exists() if user.is_authenticated else False

    def get_seller(self, obj):
        return obj.product.seller.full_name


class CategoryForSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "icon"]


class MySearchListSerializer(serializers.ModelSerializer):
    category = CategoryForSearchSerializer(read_only=True)

    class Meta:
        model = MySearch
        fields = [
            "id",
            "category",
            "search_query",
            "price_min",
            "price_max",
            "region",
            "created_at",
        ]


class MySearchCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category"
    )
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), source="region", required=False, allow_null=True
    )

    class Meta:
        model = MySearch
        fields = [
            "id",
            "category_id",
            "search_query",
            "price_min",
            "price_max",
            "region_id",
        ]


class CategoryProductSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_name(self, obj):
        if isinstance(obj, Category):
            return obj.name
        elif isinstance(obj, Ad):
            return obj.name
        return None

    def get_icon(self, obj):
        if isinstance(obj, Category):
            return obj.icon.url if obj.icon else None
        elif isinstance(obj, Ad):
            first_photo = obj.photos.first()
            return first_photo.image.url if first_photo else None
        return None

    def get_type(self, obj):
        if isinstance(obj, Category):
            return "category"
        elif isinstance(obj, Ad):
            return "product"
        return "unknown"


class ProductSearchQuerySerializer(serializers.Serializer):
    q = serializers.CharField(required=True)


class ProductCompleteSearchSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'name', 'icon']

    def get_icon(self, obj):
        return "https://admin.77.uz/media/icons/phone.svg"


class SearchCountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.IntegerField(source="category.id")
    search_count = serializers.IntegerField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True)



class PopularCategorySerializer(serializers.ModelSerializer):
    search_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "icon", "search_count", "view_count"]

    def get_search_count(self, obj):
        return getattr(obj, "total_search", 0)

    def get_view_count(self, obj):
        return getattr(obj, "total_views", 0)


class SubCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'product_count']

    def get_product_count(self, obj):
        return f"{obj.ads.count():,}"



