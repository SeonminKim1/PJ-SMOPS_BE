from django.urls import path
from art import views

# mygallery/
urlpatterns = [
    path('', views.MyGalleryAPIView.as_view()),
    # path('', views.MyGalleryAPIView.as_view()),    
    path('<art_id>', views.MyGalleryInfoAPIView.as_view()),    
]
