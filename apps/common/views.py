from drf_spectacular.utils import extend_schema
from rest_framework import generics
from .models import Page, Region, AppInfo
from .serializers import (
    PageListSerializer,
    PageDetailSerializer,
    RegionSerializer,
    AppInfoSerializer
)
from .pagination import CustomPagination
from .utils.custom_response_decorator import custom_response


@extend_schema(tags=["Common"], description="Statik sahifalar ro'yxatini olish")
@custom_response
class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    pagination_class = CustomPagination


@extend_schema(tags=["Common"], description="Ma'lum slug bo'yicha statik sahifani olish")
@custom_response
class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = 'slug'


@extend_schema(tags=["Common"], description="Viloyatlar va ularning tumanlarini ro'yxatini olish")
@custom_response
class RegionWithDistrictsView(generics.ListAPIView):
    queryset = Region.objects.prefetch_related('districts').all()
    serializer_class = RegionSerializer


@extend_schema(tags=["Common"], description="Ilova sozlamalarini olish")
@custom_response
class AppInfoView(generics.RetrieveAPIView):
    serializer_class = AppInfoSerializer

    def get_object(self):
        return AppInfo.objects.first()
