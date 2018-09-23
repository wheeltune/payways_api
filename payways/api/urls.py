from django.urls import path, include

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('auth/', include('rest_auth.urls')),
    path('auth/register/', include('rest_auth.registration.urls')),

    path('', include('payways.api.urls_api')),
    path('<int:request_user_pk>/', include('payways.api.urls_api')),
]
