"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chaining/", include("smart_selects.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),  # schema json
    path(
        "api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),  # swagger UI
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),  # redoc UI
    path("api/v1/common/", include(("common.urls", "common"), "common")),
    path("api/v1/accounts/", include(("accounts.urls", "accounts"), "accounts")),
    path("api/v1/store/", include(("store.urls", "store"), "store")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]