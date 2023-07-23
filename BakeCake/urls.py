"""BakeCake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf.urls.static import static

from shop import views
from shop.views import product_detail
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main'),
    path('catalog', views.show_catalog, name='catalog'),
    path('agreement', views.show_agreement, name='agreement'),
    # path('main', views.show_main_page, name='main'),
    path('<int:pk>', product_detail, name='product_detail'),
    path('lk', views.show_lk_page, name='lk'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('count_clicks/', views.clicks, name='count_clicks'),
    # path('pay', views.payment, name='payment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
