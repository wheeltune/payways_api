from django.urls import path

from . import views

urlpatterns = [
    # path('', views.GroupListView.as_view()),
    path('<int:pk>/', views.GroupView.as_view()),
    path('<int:pk>/members/', views.GroupMembersList.as_view()),
    # path('<int:room_pk>/things/', views.ThingsList.as_view()),
    # path('<int:room_pk>/invite/', views.GroupInviteView.as_view()),
]
