from rest_framework import generics
from .models import Page, Region, District, AppInfo
from .serializers import PageSerializer, RegionSerializer, DistrictSerializer, AppInfoSerializer


class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = 'slug'


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class RegionDetailView(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = 'pk'


class DistrictListView(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class DistrictDetailView(generics.RetrieveAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    lookup_field = 'pk'


class AppInfoListView(generics.ListAPIView):
    queryset = AppInfo.objects.all()
    serializer_class = AppInfoSerializer

    def get_object(self):
        return AppInfo.objects.first()