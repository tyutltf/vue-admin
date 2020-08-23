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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter,SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from api.views import *
from goods.views import GoodsList, GoodsInfoList, GoodsTag, GoodsProductList, GoodsImageUpload
from api.views import generateCode
from order.views import OrderView,OrderLogisticsView


ALL = {'get':'list','post':'create','put':'update','delete':'destroy'}
GET = {'get':'list'}
RET = {'get':'retrieve'}
POST = {'post':'create'}
PUT = {'put':'update'}
DEL = {'delete':'destroy'}


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('v1/api-auth/', include('rest_framework.urls'))
    # path('book/',Book.as_view({'get':'list','post':'create'})),
    # path('book/<int:pk>', Book.as_view({'get': 'retrieve'})),
    path('v1/api/code/',generateCode.as_view(),name='code'),
    path('v1/api/user/', UserInfo.as_view({**GET,**POST}), name='user'),
    path('v1/api/user/<int:pk>', UserInfo.as_view({**PUT,**GET,**DEL,**RET}), name='userUpdate'),
    path('v1/api/user/login/', UserLogin.as_view({'post': 'login_user'}), name='userLogin'),
    path('v1/api/menu/', MenuView.as_view(GET), name='menu'),
    path('v1/api/user/rolelist/', roleList.as_view({**GET,**POST}), name='roleList'),
    path('v1/api/user/role/<int:pk>/', roleList.as_view({**DEL,**RET,**PUT}), name='roledel'),
    path('v1/api/user/roleperm/', roleGroupPermView.as_view({**GET,}), name='roleperm'),
    path('v1/api/user/roleperm/<int:pk>/', roleGroupPermView.as_view({**PUT,**RET,**POST}), name='roleperm_update'),
    path('v1/api/perm/',PermissonView.as_view(ALL)),
    path('v1/api/group/', groupList.as_view(GET)),
    path('v1/api/groupPerm/', groupPermList.as_view(GET)),
    path('v1/api-token-auth/', obtain_jwt_token),
    path('v1/api-token-refresh/', refresh_jwt_token),

]
goodRouter = [
    path('v1/goods/category/<int:pk>',GoodsList.as_view({**GET,**PUT,**DEL})),
    path('v1/goods/category/', GoodsList.as_view(POST)),
    path('v1/goods/goodsinfo/<int:pk>', GoodsInfoList.as_view({**GET,**DEL,**PUT})),
    path('v1/goods/goodsinfo/', GoodsInfoList.as_view(POST)),
    path('v1/goods/goodstag', GoodsTag.as_view(POST)),
    path('v1/goods/goodstag/<int:pk>/', GoodsTag.as_view(DEL)),
    path('v1/goods/goodslist/', GoodsProductList.as_view({**GET,**POST})),
    path('v1/goods/goodslist/<int:pk>/', GoodsProductList.as_view(DEL)),
    path('v1/goods/image/upload/', GoodsImageUpload.as_view({**GET,**POST})),
    path('v1/goods/image/delete/<int:pk>/', GoodsImageUpload.as_view({**DEL})),
]

orderRouter = [
    path('v1/order/list/',OrderView.as_view(GET)),
    path('v1/order/logistics/<int:pk>/', OrderLogisticsView.as_view(RET)),

]

urlpatterns += goodRouter
urlpatterns += orderRouter
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
# route = SimpleRouter(trailing_slash=False)
# route.register(r'book',Book,)
# urlpatterns += route.urls
# print(route.urls)
