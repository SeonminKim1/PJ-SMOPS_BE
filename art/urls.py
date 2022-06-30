from django.urls import path
from art import views

# art/
urlpatterns = [
    path('product/', views.ProductAPIView.as_view()),
    path('mygallery/', views.MyGalleryAPIView.as_view()),
    # path('', views.MyGalleryAPIView.as_view()),    
    path('mygallery/<product_id>', views.MyGalleryInfoAPIView.as_view()),    
]
