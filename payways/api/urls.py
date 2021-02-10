from django.urls import path, include
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from payways.api.permissions import IsAuthenticated
from payways.rooms.permissions import IsMember


schema_view = get_schema_view(
   openapi.Info(
      title="PayWays API",
      default_version='v1',
      description="PayWays API",
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@snippets.local"),
    #   license=openapi.License(name="BSD License"),
   ),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('account/', include('rest_registration.api.urls')),

    path('contacts/', include('payways.contacts.urls')),
    path('users/', include('payways.users.urls')),
    path('rooms/', include('payways.rooms.urls')),
    path('things/', include('payways.things.urls')),

    path('token/', TokenObtainPairView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
