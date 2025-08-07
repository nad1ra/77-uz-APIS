from rest_framework import generics
from rest_framework.response import Response
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
    pagination_class = CustomPagination

    def get_serializer_context(self):
        return {'lang': self.request.headers.get('Accept-Language', 'uz')}


class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = 'slug'

    def get_serializer_context(self):
        return {'lang': self.request.headers.get('Accept-Language', 'uz')}


class RegionWithDistrictsView(generics.ListAPIView):
    queryset = Region.objects.prefetch_related('districts').all()
    serializer_class = RegionSerializer
    pagination_class = CustomPagination

    def get_serializer_context(self):
        return {'lang': self.request.headers.get('Accept-Language', 'uz')}


class AppInfoView(generics.ListAPIView):
    queryset = AppInfo.objects.all()
    serializer_class = AppInfoSerializer
    pagination_class = CustomPagination

    def get_serializer_context(self):
        return {'lang': self.request.headers.get('Accept-Language', 'uz')}
