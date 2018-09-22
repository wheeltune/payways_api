from django.urls import include, path

from . import views

urlpatterns = [
    path('<int:pk>/', views.UserView.as_view()),
    # path('<int:user_pk>/contacts/', views.ContactView.as_view())
]
