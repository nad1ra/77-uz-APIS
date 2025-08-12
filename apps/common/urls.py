from django.urls import path
from .views import PageListView, PageDetailView, RegionWithDistrictsView, AppInfoView


urlpatterns = [
    path('pages/', PageListView.as_view()),
    path('pages/<slug:slug>/', PageDetailView.as_view()),
    path('regions-with-districts/', RegionWithDistrictsView.as_view()),
    path('app-info/', AppInfoView.as_view()),
]
