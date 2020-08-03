"""vue_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from rest_framework.routers import DefaultRouter,SimpleRouter
from api.views import Book,UserLogin,MenuView
from api.views import generate_code


# GET = {'get':'list','post':'create','put':'update','delete':'destroy'}

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls'))
    # path('book/',Book.as_view({'get':'list','post':'create'})),
    # path('book/<int:pk>', Book.as_view({'get': 'retrieve'})),
    path('api/code/',generate_code,name='code'),
    path('api/user/', UserLogin.as_view({'get':'list','post':'create'}), name='user'),
    path('api/user/login/', UserLogin.as_view({'post': 'login_user'}), name='user'),
    path('api/menu/', MenuView.as_view({'get': 'list'}), name='menu'),
]

# route = SimpleRouter(trailing_slash=False)
# route.register(r'book',Book,)
# urlpatterns += route.urls
# print(route.urls)
