"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import *
from registration.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth", RegisterView.as_view(), name="register"),
    path("api/sendCoin", TransferCoinsView.as_view(), name="transfer-coins"),
    path(
        "api/buy/<str:merch_name>",
        PurchaseMerchAPIView.as_view(),
        name="purchase_merch",
    ),
    path("api/info", UserInfoAPIView.as_view(), name="user-info"),
]
