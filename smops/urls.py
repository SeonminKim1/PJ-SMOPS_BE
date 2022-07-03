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
from django.urls import path, include

from art.views import ProductsByCategoryView, ProductsByFilteringView, ProductsByArtistSearchingingView, ProductsByArtistSearchingingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('art/', include("art.urls")),
    path('mygallery/', include("mygallery.urls")),
    path('user/', include("user.urls")),
    path('ai/', include("ai.urls")),

    # 상품 Category 별 조회
    path("product/<str:category_name>/", ProductsByCategoryView.as_view()),    

    # 상품 Filtering & 검색 조회
    path("product/", ProductsByFilteringView.as_view()),
    path("product/<str:category_name>/<str:searching_text>/", ProductsByArtistSearchingingView.as_view()),

    # 상품 상세 페이지
    path("product/detail/<int:product_id>", ProductsByArtistSearchingingView.as_view())
]
