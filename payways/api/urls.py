from django.urls import path, include

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('auth/', include('rest_auth.urls')),
    path('auth/register/', include('rest_auth.registration.urls')),

    path('users/', include('payways.users.urls')),
    path('rooms/', include('payways.rooms.urls')),
    path('invites/', include('payways.invites.urls')),
    path('things/', include('payways.things.urls')),
    # path('account/', include('payways.account.urls')),
    # path('contacts/', include('payways.contacts.urls')),
]
