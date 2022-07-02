from django.urls import path
from mygallery import views

# art/
urlpatterns = [
    path('', views.ProductAPIView.as_view()),
]
