from rest_framework import generics
from .models import Page, Region, AppInfo
from .serializers import (
    PageListSerializer,
    PageDetailSerializer,
    RegionSerializer,
    AppInfoSerializer
)
from .pagination import CustomPagination


class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer


class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = 'slug'


class RegionWithDistrictsView(generics.ListAPIView):
    queryset = Region.objects.prefetch_related('districts').all()
    serializer_class = RegionSerializer


class AppInfoView(generics.RetrieveAPIView):
    queryset = AppInfo.objects.all()
    serializer_class = AppInfoSerializer
    pagination_class = CustomPagination
