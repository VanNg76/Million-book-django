"""app_project URL Configuration

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
from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from app_api.views import register_user, login_user
from app_api.views import BookView, CategoryView, UserView, AuthorView
from app_api.views import OrderView, OrderBookView
from app_api.views.inventory import InventoryView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'books', BookView, 'book')
router.register(r'categories', CategoryView, 'category')
router.register(r'users', UserView, 'user')
router.register(r'authors', AuthorView, 'author')
router.register(r'orders', OrderView, 'order')
router.register(r'orderbooks', OrderBookView, 'orderbook')
router.register(r'inventories', InventoryView, 'inventory')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]
