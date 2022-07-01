from django.urls import path
from mygallery import views


# mygallery/
urlpatterns = [
    path('', views.MyGalleryAPIView.as_view()),
    path('<product_id>', views.MyGalleryInfoAPIView.as_view()),
        
]
