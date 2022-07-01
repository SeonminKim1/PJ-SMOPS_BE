from django.urls import path
from user import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# user/
urlpatterns = [
    path('', views.UserAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
