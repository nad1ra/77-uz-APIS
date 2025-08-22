from django.db.models import Sum
from drf_spectacular.utils import extend_schema
from common.pagination import (
    AdListPagination,
    MyAdsListPagination,
    MyFavouriteProductPagination,
    MySearchPagination,
)
from common.utils.custom_response_decorator import custom_response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AdFilter
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Ad, FavouriteProduct, Category, MySearch, AdPhoto, SearchCount
from .serializers import (
    CategorySerializer,
    AdCreateSerializer,
    AdDetailSerializer,
    AdPhotoSerializer,
    FavouriteProductSerializer,
    CategoryWithChildrenSerializer,
    AdListSerializer,
    MyAdsListSerializer,
    MyAdsDetailSerializer,
    FavouriteProductListSerializer,
    MySearchListSerializer,
    MySearchCreateSerializer,
    CategoryProductSearchSerializer,
    ProductCompleteSearchSerializer,
    ProductSearchQuerySerializer,
    SearchCountSerializer,
    PopularCategorySerializer,
    SubCategorySerializer,
)
from .mixins import (
    SerializerContextMixin,
    StandardListResponseMixin,
    SuccessCreateMixin,
    SuccessDeleteMixin,
    UserFilteredQuerysetMixin,
    OwnerProtectedDeleteMixin,
)


@extend_schema(
    tags=["Store"],
    description="Barcha kategoriyalar ro‘yxatini olish",
    responses={200: CategorySerializer(many=True)},
)
@custom_response
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = AdListPagination


@extend_schema(
    tags=["Store"],
    description="Barcha ota-kategoriya va ularning bolalarini olish",
    responses={200: CategoryWithChildrenSerializer(many=True)},
)
@custom_response
class CategoryWithChildrenListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategoryWithChildrenSerializer


@extend_schema(
    tags=["Store"],
    description="Barcha subkategoriyalar ro‘yxatini olish",
    responses=SubCategorySerializer(many=True),
)
@custom_response
class SubCategoryListView(StandardListResponseMixin, generics.ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=False).order_by("name")


@extend_schema(
    tags=["Store"],
    description="E'lonlar ro‘yxatini olish (filter va pagination bilan)",
    responses={200: AdListSerializer(many=True)},
)
@custom_response
class AdListView(SerializerContextMixin, generics.ListAPIView):
    queryset = Ad.objects.all().select_related("category", "seller")
    serializer_class = AdListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = AdListPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter


@extend_schema(
    tags=["Store"],
    description="Yangi e'lon yaratish",
    request=AdCreateSerializer,
    responses={201: AdCreateSerializer},
)
@custom_response
class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all().select_related("category", "seller")
    serializer_class = AdCreateSerializer


@extend_schema(
    tags=["Store"],
    description="E'lonni olish, yangilash yoki o'chirish",
    responses={200: AdCreateSerializer},
)
@custom_response
class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all().select_related("category", "seller")
    serializer_class = AdDetailSerializer
    lookup_field = "slug"


@extend_schema(
    tags=["Store"],
    description="Sevimli mahsulot qo‘shish",
    request=FavouriteProductSerializer,
    responses={201: FavouriteProductSerializer},
)
@custom_response
class FavouriteProductCreateView(SuccessCreateMixin, generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all().select_related("product")
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    success_message = "Sevimli mahsulot muvaffaqiyatli qo‘shildi"


@extend_schema(
    tags=["Store"],
    description="Sevimli mahsulotni ID orqali qo‘shish",
    request=FavouriteProductSerializer,
    responses={201: FavouriteProductSerializer},
)
@custom_response
class FavouriteProductCreateByIdView(SuccessCreateMixin, generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.AllowAny]
    success_message = "Sevimli mahsulot muvaffaqiyatli qo‘shildi"


@extend_schema(
    tags=["Store"],
    description="Sevimli mahsulotni o'chirish",
    responses={204: None},
)
@custom_response
class FavouriteProductDeleteView(UserFilteredQuerysetMixin, generics.DestroyAPIView):
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        product_id = self.kwargs.get("pk")
        return get_object_or_404(FavouriteProduct, id=product_id, user=self.request.user)


@extend_schema(
    tags=["Store"],
    description="Sevimli mahsulotni ID bo‘yicha o‘chirish",
    responses={204: None},
)
@custom_response
class FavouriteProductDeleteByIdView(SuccessDeleteMixin, generics.DestroyAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"
    success_message = "Sevimli mahsulot muvaffaqiyatli o‘chirildi"
    not_found_message = "Favourite product not found"


@extend_schema(
    tags=["Store"],
    description="Hozirgi foydalanuvchining sevimli mahsulotlarini ro‘yxatini olish. `category` query param orqali filtr qilish mumkin",
    responses={200: FavouriteProductListSerializer(many=True)},
)
@custom_response
class MyFavouriteProductListView(generics.ListAPIView):
    serializer_class = FavouriteProductListSerializer
    pagination_class = MyFavouriteProductPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        category_id = self.request.query_params.get("category")
        queryset = FavouriteProduct.objects.filter(user=self.request.user)

        if category_id:
            queryset = queryset.filter(product__category_id=category_id)

        return (
            queryset
            .select_related("product", "product__seller", "product__address")
            .prefetch_related("product__photos")
            .order_by("-product__published_at")
        )


@extend_schema(
    tags=["Store"],
    description=(
        "Sevimli mahsulotlar ro‘yxatini olish. "
        "`device_id` query param orqali filtrlash mumkin. "
        "Agar foydalanuvchi login qilgan bo‘lsa va `device_id` berilmagan bo‘lsa, "
        "foydalanuvchining sevimli mahsulotlari qaytariladi. "
        "Agar login qilmagan va `device_id` berilmagan bo‘lsa, natija bo‘sh bo‘ladi."
    ),
    responses={200: FavouriteProductListSerializer(many=True)},
)
@custom_response
class MyFavouriteProductByIdView(generics.ListAPIView):
    serializer_class = FavouriteProductListSerializer
    pagination_class = MyFavouriteProductPagination

    def get_queryset(self):
        device_id = self.request.query_params.get("device_id")
        queryset = FavouriteProduct.objects.all()

        if device_id:
            queryset = queryset.filter(device_id=device_id)
        elif self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        else:
            queryset = queryset.none()

        return (
            queryset.select_related("product", "product__seller", "product__address")
            .prefetch_related("product__photos")
            .order_by("-id")
        )


@extend_schema(
    tags=["Store"],
    description="Hozirgi foydalanuvchining barcha e'lonlari ro‘yxatini olish (filter va pagination bilan)",
    responses={200: AdListSerializer(many=True)},
)
@custom_response
class MyAdsListView(SerializerContextMixin, generics.ListAPIView):
    serializer_class = AdListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyAdsListPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    def get_queryset(self):
        return (
            Ad.objects.filter(seller=self.request.user)
            .select_related("address")
            .order_by("-published_at")
        )


@extend_schema(
    tags=["Store"],
    description="Hozirgi foydalanuvchining bitta e'lonini olish, yangilash yoki o‘chirish",
    responses={200: MyAdsListSerializer},
)
@custom_response
class MyAdsDetailView(SerializerContextMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyAdsDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Ad.objects.filter(seller=self.request.user)


@extend_schema(
    tags=["Store"],
    description="Mahsulot tafsilotlarini yuklab olish",
    responses={200: AdDetailSerializer},
)
@custom_response
class ProductDownloadView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = "slug"


@extend_schema(
    tags=["Store"],
    description="Mahsulotga rasm qo‘shish",
    request=AdPhotoSerializer,
    responses={201: AdPhotoSerializer},
)
@custom_response
class ProductImageCreateView(generics.CreateAPIView):
    serializer_class = AdPhotoSerializer
    queryset = AdPhoto.objects.all()
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=["Store"],
    description="Foydalanuvchining qidiruv tarixini olish. Foydalanuvchi login qilgan bo‘lishi kerak.",
    responses={200: MySearchListSerializer(many=True)},
)
@custom_response
class MySearchListView(generics.ListAPIView):
    serializer_class = MySearchListSerializer
    pagination_class = MySearchPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MySearch.objects.filter(user=self.request.user).order_by("-created_at")


@extend_schema(
    tags=["Store"],
    description="Foydalanuvchi qidiruvini yaratish. Foydalanuvchi login qilgan bo‘lishi kerak.",
    request=MySearchCreateSerializer,
    responses={201: MySearchCreateSerializer},
)
@custom_response
class MySearchCreateView(generics.CreateAPIView):
    serializer_class = MySearchCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    tags=["Store"],
    description="Foydalanuvchining qidiruvini ID orqali o‘chirish. Foydalanuvchi faqat o‘z qidiruvini o‘chira oladi.",
    responses={204: None}
)
@custom_response
class MySearchDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(MySearch, id=self.kwargs.get('id'), user=request.user)
        instance.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Store"],
    description="Foydalanuvchining qidiruvini ko‘rish yoki o‘chirish. Foydalanuvchi faqat o‘z qidiruvlarini ko‘ra oladi.",
    responses={200: MySearchListSerializer},
)
@custom_response
class MySearchDetailView(OwnerProtectedDeleteMixin, generics.RetrieveDestroyAPIView):
    queryset = MySearch.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return MySearch.objects.filter(user=self.request.user)


@extend_schema(
    tags=["Store"],
    description="Kategoriya va mahsulotlarni qidirish",
    responses={200: CategoryProductSearchSerializer(many=True)},
)
@custom_response
class CategoryProductSearchView(StandardListResponseMixin, generics.ListAPIView):
    serializer_class = CategoryProductSearchSerializer

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        categories = list(Category.objects.filter(name__icontains=q))
        products = list(Ad.objects.filter(name__icontains=q, status="active"))
        return categories + products


@extend_schema(
    tags=["Store"],
    description="Mahsulotlarni to‘liq filter yordamida qidirish",
    responses={200: ProductCompleteSearchSerializer(many=True)},
)
@custom_response
class ProductCompleteSearchView(generics.ListAPIView):
    serializer_class = ProductCompleteSearchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    def get_queryset(self):
        serializer = ProductSearchQuerySerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        q = serializer.validated_data["q"]
        return Ad.objects.filter(name__icontains=q, status="active")


@extend_schema(
    tags=["Store"],
    description="Kategoriyaning qidiruv sonini 1 ga oshiradi",
    responses={200: SearchCountSerializer},
)
@custom_response
class SearchCountIncreaseView(generics.RetrieveAPIView):
    serializer_class = SearchCountSerializer
    lookup_field = "id"

    def get_queryset(self):
        return SearchCount.objects.all()

    def get(self, request, *args, **kwargs):
        category_id = self.kwargs.get("id")
        category = get_object_or_404(Category, id=category_id)
        obj, _ = SearchCount.objects.get_or_create(category=category)
        obj.search_count += 1
        obj.save()
        return Response(self.get_serializer(obj).data)


@extend_schema(
    tags=["Store"],
    description="Mashhur kategoriyalar ro‘yxatini olish",
    responses=PopularCategorySerializer(many=True),
)
@custom_response
class PopularCategoryListView(StandardListResponseMixin, generics.ListAPIView):
    serializer_class = PopularCategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(
            total_search=Sum("search_counts__search_count"),
            total_views=Sum("ads__view_count"),
        ).order_by("-total_views")




