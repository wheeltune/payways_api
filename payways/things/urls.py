from django.urls import include, path

from . import views

urlpatterns = [
    path('<int:thing_pk>/', views.ThingView.as_view())
]
