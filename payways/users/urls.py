from django.urls import include, path

from . import views

urlpatterns = [
    path('<int:pk>/', views.UserView.as_view()),
    path('<int:pk>/rooms/', include('payways.rooms.urls')),
    # path('<int:pk>/contacts/', views.ContactView.as_view()),
    # path('<int:pk>/debts/', include('payways.debts.urls'))
]
