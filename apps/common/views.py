from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Page, Region, AppInfo
from .serializers import (
    PageListSerializer, PageDetailSerializer,
    RegionSerializer, AppInfoSerializer
)
from .pagination import CustomPagination


class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    pagination_class = CustomPagination


class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = 'slug'


class RegionWithDistrictsView(APIView):
    def get(self, request):
        regions = Region.objects.prefetch_related('districts').all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)


class AppInfoView(APIView):
    def get(self, request):
        app_info = AppInfo.objects.first()
        serializer = AppInfoSerializer(app_info)
        return Response(serializer.data)
