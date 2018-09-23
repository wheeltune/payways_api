from django.urls import path, include

urlpatterns = [
    path('users/', include('payways.users.urls')),
    path('rooms/', include('payways.rooms.urls')),
    path('invites/', include('payways.invites.urls')),
    path('things/', include('payways.things.urls')),
    # path('account/', include('payways.account.urls')),
    # path('contacts/', include('payways.contacts.urls')),
]
