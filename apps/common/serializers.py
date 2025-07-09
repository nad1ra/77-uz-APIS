from rest_framework import serializers
from .models import Page, Region, District, AppInfo

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['guid', 'slug', 'title', 'content', 'created_time', 'updated_time']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class AppInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInfo
        fields = [
            'id',
            'phone',
            'support_email',
            'working_hours',
            'app_version',
            'maintenance_mode'
        ]