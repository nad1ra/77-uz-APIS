from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Ad, FavouriteProduct
from .serializers import (
    CategorySerializer, AdCreateSerializer, FavouriteProductSerializer
)
from common.utils.custom_response_decorator import custom_response
from .models import Category
from .serializers import CategoryWithChildrenSerializer


@custom_response
class CategoryWithChildrenListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategoryWithChildrenSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all().select_related("category", "seller")
    serializer_class = AdCreateSerializer


class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all().select_related("category", "seller")
    serializer_class = AdCreateSerializer
    lookup_field = "slug"


class FavouriteProductListCreateView(generics.ListCreateAPIView):
    queryset = FavouriteProduct.objects.all().select_related("product")
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "success": True,
                "message": "Sevimli mahsulot muvaffaqiyatli qo'shildi",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class FavouriteProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FavouriteProduct.objects.all().select_related("product")
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.AllowAny]


class FavouriteProductDeleteByIdView(generics.DestroyAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        try:
            favourite = self.get_object()
            favourite.delete()
            return Response(
                {"success": True, "message": "sevimli mahsulot muvaffaqiyatli o'chirildi"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except FavouriteProduct.DoesNotExist:
            return Response(
                {"success": False, "message": "Favourite product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )



