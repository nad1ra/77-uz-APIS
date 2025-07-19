from rest_framework import serializers
from .models import Page, Region, District, AppInfo
from django.utils.translation import get_language


class PageListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['slug', 'title']

    def get_title(self, obj):
        lang = get_language() or 'uz'
        return getattr(obj, f"title_{lang}", obj.title)


class PageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['slug', 'title', 'content', 'created_time', 'updated_time']

    def get_title(self, obj):
        lang = get_language() or 'uz'
        return getattr(obj, f"title_{lang}", obj.title)

    def get_content(self, obj):
        lang = get_language() or 'uz'
        return getattr(obj, f"content_{lang}", obj.content)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'id',
            'name_uz',
            'name_ru',
        ]


class RegionSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True)

    class Meta:
        model = Region
        fields = [
            'id',
            'name',
            'districts'
        ]


class AppInfoSerializer(serializers.ModelSerializer):
    working_hours = serializers.SerializerMethodField()

    class Meta:
        model = AppInfo
        fields = [
            'phone',
            'support_email',
            'working_hours',
            'app_version',
            'maintenance_mode',
        ]

    def get_working_hours(self, obj):
        lang = get_language()
        if lang == 'ru':
            return obj.working_hours_ru
        return obj.working_hours_uz