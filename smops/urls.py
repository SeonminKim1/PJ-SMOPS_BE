"""smops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
=======
from django.urls import path
from user.views import TestUserView
from art.views import TestProductView
>>>>>>> e370dfcc22eb4e3eaa5fa9c85884cbff74c47a88

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    path('mygallery/', include("art.urls"))
=======
    path("admin/", admin.site.urls),
<<<<<<< HEAD
>>>>>>> 31e2d83591775702a64ebd0c049237ba0870fce0
=======




    ## Test 용 URL 입니다.
    path("get_users/", TestUserView.as_view()),
    path('get_products/', TestProductView.as_view()),
>>>>>>> e370dfcc22eb4e3eaa5fa9c85884cbff74c47a88
]
