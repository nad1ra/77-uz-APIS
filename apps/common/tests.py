from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Page, Region, District, AppInfo


class CommonAPITests(APITestCase):
    def setUp(self):
        # Page yaratish
        self.page = Page.objects.create(title="Test Page", content="Test content")

        # Region va District yaratish
        self.region = Region.objects.create(name="Test Region")
        self.district1 = District.objects.create(name="District 1", region=self.region)
        self.district2 = District.objects.create(name="District 2", region=self.region)

        # AppInfo yaratish
        self.app_info = AppInfo.objects.create(
            phone="+998901234567",
            support_email="support@test.com",
            working_hours="9:00-18:00",
            app_version="1.0.0",
            maintenance_mode=False
        )

    def test_page_list(self):
        url = reverse('page-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
        self.assertEqual(response.data['results'][0]['slug'], self.page.slug)

    def test_page_detail(self):
        url = reverse('page-detail', args=[self.page.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.page.slug)
        self.assertEqual(response.data['title'], self.page.title)
        self.assertEqual(response.data['content'], self.page.content)

    def test_region_with_districts(self):
        url = reverse('regions-with-districts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        region_data = response.data[0]
        self.assertEqual(region_data['id'], self.region.id)
        self.assertEqual(region_data['name'], self.region.name)
        self.assertEqual(len(region_data['districts']), 2)
        self.assertEqual(region_data['districts'][0]['name'], self.district1.name)

    def test_app_info(self):
        url = reverse('app-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], self.app_info.phone)
        self.assertEqual(response.data['support_email'], self.app_info.support_email)
        self.assertEqual(response.data['working_hours'], self.app_info.working_hours)
        self.assertEqual(response.data['app_version'], self.app_info.app_version)
        self.assertEqual(response.data['maintenance_mode'], self.app_info.maintenance_mode)
