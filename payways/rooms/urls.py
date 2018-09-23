from django.urls import path

from . import views

urlpatterns = [
    path('', views.RoomsListView.as_view()),
    path('<int:room_pk>/', views.RoomView.as_view()),
    path('<int:room_pk>/members/', views.RoomMembersListView.as_view()),
    # path('<int:room_pk>/things/', views.ThingsList.as_view()),
    # path('<int:room_pk>/invite/', views.GroupInviteView.as_view()),
]