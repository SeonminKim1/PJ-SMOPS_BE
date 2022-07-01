from django.urls import path
from . import views

# ai/
urlpatterns = [
    path('', views.AiProductView.as_view()),
]