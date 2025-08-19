from django.urls import path
from . import views

urlpatterns = [
    path('categories-with-children/', views.CategoryWithChildrenListView.as_view(), name='categories-with-children'),
    path("category/", views.CategoryListView.as_view(), name="category-list"),
    path("ads/", views.AdCreateView.as_view(), name="ad-create"),
    path("ads/<slug:slug>/", views.AdDetailView.as_view(), name="ad-detail"),
    path("favourites/", views.FavouriteProductListCreateView.as_view(), name="favourite-list-create"),
    path("favourites/<int:pk>/", views.FavouriteProductDetailView.as_view(), name="favourite-detail"),
    path(
        "favourites/<int:id>/delete/",
        views.FavouriteProductDeleteByIdView.as_view(),
        name="favourite-delete-by-id",
    ),
]

