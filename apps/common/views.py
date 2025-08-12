from rest_framework import generics
from .models import Page, Region, AppInfo
from .serializers import (
    PageListSerializer,
    PageDetailSerializer,
    RegionSerializer,
    AppInfoSerializer
)
from .pagination import CustomPagination
from drf_yasg.utils import swagger_auto_schema
from . import openapi_schema as schemas


class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(responses={200: schemas.page_list_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = 'slug'

    @swagger_auto_schema(responses={200: schemas.page_detail_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RegionWithDistrictsView(generics.ListAPIView):
    queryset = Region.objects.prefetch_related('districts').all()
    serializer_class = RegionSerializer

    @swagger_auto_schema(responses={200: schemas.region_with_districts_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AppInfoView(generics.RetrieveAPIView):
    serializer_class = AppInfoSerializer

    @swagger_auto_schema(responses={200: schemas.setting_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return AppInfo.objects.first()
