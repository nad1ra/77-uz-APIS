from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    limit_query_param = "limit"
    offset_query_param = "offset"


class PageListPagination(CustomPagination):
    page_size = 10


class AdListPagination(CustomPagination):
    page_size = 20


class MyAdsListPagination(CustomPagination):
    page_size = 10


class MyFavouriteProductPagination(CustomPagination):
    page_size = 10


class MySearchPagination(CustomLimitOffsetPagination):
    pass


class SearchListPagination(CustomLimitOffsetPagination):
    pass