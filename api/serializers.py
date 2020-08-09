import traceback
from itertools import chain

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission,Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,Serializer
from api import models



class Book_Serializer(ModelSerializer):
    # create_time = serializers.SerializerMethodField()
    # date = serializers.SerializerMethodField('get_create_date')
    # def get_create_time(self,obj):
    #     print(obj)
    #     return obj
    uname = serializers.CharField(source='name',)
    date = serializers.DateTimeField(source='create_date',format='%Y-%m-%d %H:%M%S')


    class Meta:
        model = models.Book
        fields = ['id','uname','date']


class UserSerializer(ModelSerializer):
    '''用户列表'''

    # group = serializers.SerializerMethodField('get_group')
    # def get_group(self,obj):
    #     return [obj.id,]
    group = serializers.IntegerField(source='role.id')
    role = serializers.CharField(source='role.name')

    class Meta:
        fields = ('id','username','email','telephone','group','is_active','role')
        model = models.User


class userCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    # def validate(self, attrs):
    #     if attrs['password'].__len__()>5:
    #         raise serializers.ValidationError('密码长度过段')

    class Meta:
        fields = '__all__'
        model = models.User


class MenuChildSerialiser(ModelSerializer):
    '''子菜单'''

    class Meta:
        fields = ('id', 'name','url')
        model = models.MenuChild

class MenuSerialiser(ModelSerializer):
    '''
    展示菜单及子菜单
    '''

    # children = serializers.SerializerMethodField('get_child')
    # def get_child(self,obj):
    #     return MenuChildSerialiser(instance=obj).data
    children = MenuChildSerialiser(many=True,read_only=True)

    class Meta:
        fields = ('id','name','children')
        model = models.Menu
        depth = 1

class roleSerializer(ModelSerializer):
    '''角色列表'''

    def create(self, validated_data):
        '''添加角色权限'''
        obj = super(roleSerializer, self).create(validated_data)
        for group in obj.groups.all():
            obj.permlist.add(*group.permissions.all())
        return obj

    def update(self, instance, validated_data):
        '''更新用户权限'''
        obj = super(roleSerializer, self).update(instance,validated_data)
        obj.permlist.clear()
        for group in obj.groups.all():
            obj.permlist.add(*group.permissions.all())
        return obj


    class Meta:
        fields = ('id','name','info','groups')
        model = models.Role



class PermSerializer(ModelSerializer):
    '''权限列表'''
    content_type = serializers.CharField(source='content_type.app_label')

    class Meta:
        fields = ('id','content_type','codename','name')
        model = Permission

class GroupBaseSerializer(ModelSerializer):

    class Meta:
        fields = ('id','name')
        model = Group

class GroupSerializer(GroupBaseSerializer):
    # permissions = serializers.SerializerMethodField('get_perm')
    #
    # def get_perm(self,obj):
    #     return obj.permissions.all().values('id','name')

    class Meta:
        # fields = ('id','name','permissions')
        fields = ('id','name')
        model = Group

class PermBaseSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id','name')

class RoleGroupPermSerializer(ModelSerializer):
    '''展示角色下所有分组权限'''
    # groups = GroupSerializer(many=True,read_only=True)
    # permlist = permListSerializer(many=True,read_only=True)
    groups = serializers.SerializerMethodField('get_group_perm_list')
    def get_group_perm_list(self,obj):
        resp = obj.groups.all()
        values = resp.values()
        obj_perm = set(obj.permlist.all())
        for i,k in zip(resp,values):
            j = obj_perm & set(i.permissions.all())
            k['permissions'] = [PermBaseSerializer(i).data for i in j]
        return values

    class Meta:
        fields = ('id','name','info','groups',)
        model = models.Role
