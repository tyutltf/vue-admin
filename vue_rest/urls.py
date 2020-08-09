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
from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter,SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from api.views import *
from api.views import generateCode


ALL = {'get':'list','post':'create','put':'update','delete':'destroy'}
GET = {'get':'list'}
RET = {'get':'retrieve'}
POST = {'post':'create'}
PUT = {'put':'update'}
DEL = {'delete':'destroy'}
router = DefaultRouter()
router.register('/v1',roleList)
print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls'))
    # path('book/',Book.as_view({'get':'list','post':'create'})),
    # path('book/<int:pk>', Book.as_view({'get': 'retrieve'})),
    path('api/code/',generateCode.as_view(),name='code'),
    path('api/user/', UserInfo.as_view({**GET,**POST}), name='user'),
    path('api/user/<int:pk>', UserInfo.as_view({'put':'update','get':'retrieve','delete':'destroy'}), name='userUpdate'),
    path('api/user/login/', UserLogin.as_view({'post': 'login_user'}), name='userLogin'),
    path('api/menu/', MenuView.as_view({'get': 'list'}), name='menu'),
    path('api/user/rolelist/', roleList.as_view({**GET,**POST}), name='roleList'),
    path('api/user/role/<int:pk>/', roleList.as_view({**DEL,**RET,**PUT}), name='roledel'),
    path('api/user/roleperm/', roleGroupPermView.as_view({**GET,}), name='roleperm'),
    path('api/user/roleperm/<int:pk>/', roleGroupPermView.as_view({**PUT,**RET,**POST}), name='roleperm_update'),
    path('api/perm/',PermissonView.as_view(ALL)),
    path('api/group/', groupList.as_view(GET)),
    path('api/groupPerm/', groupPermList.as_view(GET)),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),

]

# route = SimpleRouter(trailing_slash=False)
# route.register(r'book',Book,)
# urlpatterns += route.urls
# print(route.urls)
