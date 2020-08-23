from datetime import datetime
from django.contrib.auth import authenticate
from django.http.response import HttpResponse
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from api.models import Book, User, Menu, Role
from api.serializers import *
from utils.gnerate_code import gen_capthca
from utils.common import ResDict, get_token, hander_error
from django_redis import get_redis_connection
from django_filters import rest_framework as filters
import io, django_filters


class filterUser(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', ]


class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 5


class BaseViewSet(ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        return Response(ResDict(resp.status_code, data=resp.data))

    def destroy(self, request, *args, **kwargs):
        try:
            resp = super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(ResDict(400, msg=str(e)))
        else:
            return Response(ResDict(200, msg='删除成功'))

    def list(self, request, *args, **kwargs):
        try:
            resp = super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(ResDict(400, msg=str(e)))
        else:
            return Response(ResDict(200, data=resp.data), status=resp.status_code)


class generateCode(APIView):
    permission_classes = ()

    def get(self, request):
        code = request.query_params.get('code_id')
        con = get_redis_connection()
        text, image = gen_capthca()
        con.set(code, text, 300)
        fp = io.BytesIO()
        image.save(fp, 'png')
        fp.seek(0)
        response = HttpResponse(content=fp, content_type='application/x-plt')
        return response


class roleList(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = roleSerializer
    pagination_class = LargeResultsSetPagination

    def create(self, request, *args, **kwargs):
        request.data.update(groups=request.data.get('checkList', None))
        obj = roleSerializer(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response(ResDict(200, data=obj.data))
        else:
            return Response(ResDict(400, msg=hander_error(obj.errors)))

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(instance=obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ResDict(200, msg='修改成功'))
        else:
            return Response(ResDict(400, msg=hander_error(serializer.errors)))


class UserLogin(ModelViewSet):
    permission_classes = ()

    def login_user(self, request, *args, **kwargs):
        con = get_redis_connection()
        code_id = request.data.get('code_id', None)
        code = request.data.get('code', None)
        username = request.data.get('username', None)
        pwd = request.data.get('pwd', None)
        if not code:
            return Response(ResDict(400, '验证码缺失'))

        _code = con.get(str(code_id))
        if not _code:
            return Response(ResDict(400, '验证码过期'))

        if _code.decode().lower() != code.lower():
            print(_code, code)
            return Response(ResDict(400, '验证码错误'))

        if not all([username, pwd]):
            return Response(ResDict(400, '用户名或密码缺失'))

        user = authenticate(request, username=username, password=pwd)
        if user is not None:
            # login(request,user)
            token = get_token(user)
            con.delete(code_id)
            return Response(ResDict(200, '登录成功', data={'username': user.username, 'token': token}))
        else:
            return Response(ResDict(400, '用户名或密码错误'))


class UserInfo(BaseViewSet):
    queryset = User.objects.all().prefetch_related('groups')
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = filterUser

    def create(self, request, *args, **kwargs):
        pwd1 = request.data.get('password')
        pwd2 = request.data.get('password2')
        if pwd1 != pwd2:
            return Response(ResDict(400, msg='两次密码不一致'))

        request.data['role'] = request.data.pop('group', None)
        serializer = userCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response(ResDict(400, msg='数据库错误'))
            return Response(ResDict(200, data=serializer.data))
        else:
            err_message = hander_error(serializer.errors)
            return Response(ResDict(400, msg=err_message))

    def update(self, request, *args, **kwargs):
        try:
            if 'group' in request.data:
                request.data['role'] = request.data.pop('group')
            resp = User.objects.filter(id=kwargs['pk']).update(**request.data)
        except Exception as e:
            return Response(ResDict(400, msg=str(e)))
        else:
            if resp == 1:
                return Response(ResDict(200, msg='更新成功'))
            else:
                return Response(ResDict(400, msg='更新失败'))


class MenuView(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerialiser
    pagination_class = None

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        return Response(ResDict(200, data=resp.data))


class PermissonView(BaseViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermSerializer


class roleGroupPermView(BaseViewSet):
    queryset = Role.objects.all().prefetch_related('groups')
    serializer_class = RoleGroupPermSerializer

    def get_group_perm_list(self, obj):
        resp = obj.groups.all()
        values = resp.values()
        obj_perm = set(obj.permlist.all())
        for i, k in zip(resp, values):
            j = obj_perm & set(i.permissions.all())
            k['permissions'] = [PermBaseSerializer(i).data for i in j]
        return values

    def update(self, request, *args, **kwargs):
        group_id = request.data.get('group')
        perm_id = request.data.get('perm')
        role = self.get_object()
        if group_id and perm_id:
            role.permlist.remove(Permission.objects.get(id=perm_id))
        elif group_id:
            role.groups.remove(Group.objects.get(id=group_id))

        resp = self.get_group_perm_list(role)
        return Response(ResDict(200, data=resp))

    def create(self, request, *args, **kwargs):
        role = self.get_object()
        perm_list = request.data.get('permlist', None)
        if perm_list is not None:
            role.permlist.clear()
            role.permlist.add(*Permission.objects.filter(id__in=perm_list))
            return Response(ResDict(200,msg='更新成功'))
        else:
            return Response(ResDict(400,msg='更新失败,权限id缺失'))



class groupList(BaseViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupBaseSerializer
    pagination_class = None




class groupPermList(BaseViewSet):
    queryset = Group.objects.all()
    serializer_class = groupPermSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        role_id = request.query_params.get('role_id')
        resp = super(groupPermList, self).list(request,*args,**kwargs)
        role = Role.objects.get(id=role_id)
        checklist = role.permlist.values_list('id',flat=True)
        resp.data['data'] = {'checklist':checklist,'results':resp.data['data']}
        return resp



class Book(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = Book_Serializer
    pagination_class = LargeResultsSetPagination

    def create(self, request, *args, **kwargs):
        request.data['date'] = datetime.today()
        try:
            resp = super().create(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return Response(resp.data)
        else:
            setattr(resp.data, 'code', 200)
            return Response(data=resp.data)
