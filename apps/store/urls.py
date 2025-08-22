from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("categories-with-children/", views.CategoryWithChildrenListView.as_view(), name="categories-with-children"),

    path("ads/", views.AdCreateView.as_view(), name="ad-create"),
    path("ads/<slug:slug>/", views.AdDetailView.as_view(), name="ad-detail"),
    path("list/ads/", views.AdListView.as_view(), name="ad-list"),
    path("my-ads/", views.MyAdsListView.as_view(), name="my-ads-list"),
    path("my-ads/<int:id>/", views.MyAdsDetailView.as_view(), name="my-ads-detail"),

    path("favourite-product/create/", views.FavouriteProductCreateView.as_view(), name="favourite-create"),
    path("favourite-product/<int:pk>/delete/", views.FavouriteProductDeleteView.as_view(), name="favourite-product-delete"),
    path("favourite-product-by-id/<int:id>/delete/", views.FavouriteProductDeleteByIdView.as_view(), name="favourite-product-delete-by-id"),
    path("my-favourite-products/", views.MyFavouriteProductListView.as_view(), name="my-favourite-products"),
    path("my-favourite-products-by-id/", views.MyFavouriteProductByIdView.as_view(), name="my-favourite-products-by-id"),
    path("favourite-product-create-by-id/", views.FavouriteProductCreateByIdView.as_view(), name="favourite-product-create-by-id"),

    path("my-search/create/", views.MySearchCreateView.as_view(), name="my-search-create"),
    path("my-search/list/", views.MySearchListView.as_view(), name="my-search-list"),
    path('my-search/<int:id>/delete/', views.MySearchDeleteView.as_view(), name='my-search-delete'),
    path('product-download/<slug:slug>/', views.ProductDownloadView.as_view(), name='product-download'),
    path('product-image-create/', views.ProductImageCreateView.as_view(), name='product-image-create'),
    path('search/category-product/', views.CategoryProductSearchView.as_view(), name='category-product-search'),
    path('search/complete/', views.ProductCompleteSearchView.as_view(), name='product-complete-search'),
    path("search/count-increase/<int:id>/", views.SearchCountIncreaseView.as_view(), name="search-count-increase"),

    path("search/populars/", views.PopularCategoryListView.as_view(), name="populars"),
    path("sub-categories/", views.SubCategoryListView.as_view(), name="sub-category-list"),
]
