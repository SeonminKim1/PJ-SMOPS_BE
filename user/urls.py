from django.urls import path
from user import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from user.views import OnlyAuthenticatedUserView

# user/token_obtain_pair
urlpatterns = [
    path('', views.UserAPIView.as_view(), name="user_view"),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('api/authonly/', OnlyAuthenticatedUserView.as_view()),
]
