# common/openapi_schema.py
from drf_yasg import openapi

# -------- Page list --------
page_list_response = openapi.Response(
    description="List of pages (paginated)",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=100),
            "next": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                example="https://api.example.com/pages/?page=2",
            ),
            "previous": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, nullable=True, example=None
            ),
            "results": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "slug": openapi.Schema(type=openapi.TYPE_STRING, example="about-us"),
                        "title": openapi.Schema(type=openapi.TYPE_STRING, example="About Us"),
                    },
                ),
            ),
        },
    ),
)

# -------- Page detail --------
page_detail_response = openapi.Response(
    description="Detailed page information",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "slug": openapi.Schema(type=openapi.TYPE_STRING, example="about-us"),
            "title": openapi.Schema(type=openapi.TYPE_STRING, example="About Us"),
            "content": openapi.Schema(
                type=openapi.TYPE_STRING, example="<p>Company information...</p>"
            ),
            "created_at": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
                example="2025-08-11T12:00:00Z",
            ),
            "updated_at": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
                example="2025-08-11T12:30:00Z",
            ),
        },
    ),
)

# -------- Region with districts --------
region_with_districts_response = openapi.Response(
    description="List of regions with their districts",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Tashkent"),
                "districts": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Yakkasaroy"),
                        },
                    ),
                ),
            },
        ),
    ),
)

# -------- App info --------
setting_response = openapi.Response(
    description="App Info",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "phone": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
            "support_email": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, example="support@example.com"
            ),
            "app_version": openapi.Schema(type=openapi.TYPE_STRING, example="1.0.0"),
            "maintenance_mode": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
            "working_hours": openapi.Schema(
                type=openapi.TYPE_STRING, example="Mon-Fri 09:00-18:00"
            ),
        },
    ),
)