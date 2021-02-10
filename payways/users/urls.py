from django.urls import include, path

from . import views


urlpatterns = [
    path('<int:user_pk>/', views.UserView.as_view()),
    path('search/', views.UsersSearchView.as_view()),
    # path('', views.ContactsListView.as_view()),
    # path('<int:user_pk>/rooms/', views.RoomsInCommonListView.as_view()),
    # path('<int:pk>/rooms/', views.UserRoomListView.as_view()),
    # path('<int:pk>/debts/', include('payways.debts.urls'))
]
