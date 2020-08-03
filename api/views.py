from datetime import datetime
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from api.models import Book, User,Menu,MenuChild
from api.serializers import Book_Serializer,UserSerializer,MenuSerialiser
from utils.gnerate_code import gen_capthca
from utils.common import record,ResDict
from django_redis import get_redis_connection
from django_filters import rest_framework as filters
import io,django_filters

class filterUser(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['username',]

class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 5

@record()
def generate_code(request):
    code = request.GET.get('code_id')
    con = get_redis_connection()
    text,image = gen_capthca()
    con.set(code,text,300)
    fp = io.BytesIO()
    image.save(fp,'png')
    fp.seek(0)
    response = HttpResponse(content=fp,content_type='application/x-plt')
    return response

class UserLogin(ModelViewSet):
    queryset = User.objects.all().prefetch_related('groups')
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = filterUser

    def list(self,request,*args,**kwargs):

        resp = super().list(request,*args,**kwargs)
        return Response(ResDict(200,data=resp.data),status=resp.status_code)


    def login_user(self,request,*args,**kwargs):
        con = get_redis_connection()
        code_id = request.data.get('code_id',None)
        code = request.data.get('code',None)
        username = request.data.get('username',None)
        pwd = request.data.get('pwd',None)
        print(request.data)
        if not code:
            return Response(ResDict(400,'验证码缺失'))

        _code = con.get(str(code_id))
        if not _code:
            return Response(ResDict(400,'验证码过期'))

        if  _code.decode().lower() != code.lower():
            print(_code,code)
            return Response(ResDict(400,'验证码错误'))

        if not all([username,pwd]):
            return Response(ResDict(400,'用户名或密码缺失'))


        user = authenticate(request,username=username,password=pwd)
        if user is not None:
            login(request,user)
            con.delete(code_id)
            return Response(ResDict(200,'登录成功',{'username':user.username}))
        else:
            return Response(ResDict(400,'用户名或密码错误'))


class MenuView(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerialiser
    pagination_class = None

    def list(self,request,*args,**kwargs):
        resp = super().list(request,*args,**kwargs)
        return Response(ResDict(200,data=resp.data))



class Book(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = Book_Serializer
    pagination_class = LargeResultsSetPagination


    def create(self, request, *args, **kwargs):
        request.data['date'] = datetime.today()
        try:
            resp = super().create(request,*args,**kwargs)
        except Exception as e:
            print(e)
            return Response(resp.data)
        else:
            setattr(resp.data,'code',200)
            return Response(data=resp.data)