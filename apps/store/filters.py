import django_filters
from .models import Ad


class AdFilter(django_filters.FilterSet):
    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    seller_id = django_filters.NumberFilter(field_name="seller_id")
    district_id = django_filters.NumberFilter(field_name="seller__district_id")
    region_id = django_filters.NumberFilter(field_name="seller__region_id")
    category_ids = django_filters.BaseInFilter(field_name="category_id", lookup_expr="in")
    status = django_filters.ChoiceFilter(field_name="status", choices=Ad.Status.choices)

    class Meta:
        model = Ad
        fields = [
            "price__gte",
            "price__lte",
            "seller_id",
            "district_id",
            "region_id",
            "category_ids",
            "status",
        ]
