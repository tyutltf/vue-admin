import traceback
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission,Group
from utils.common import filter_username
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,Serializer
from api import models
import pandas as pd

from goods.models import GoodsImage


class Book_Serializer(ModelSerializer):

    uname = serializers.CharField(source='name',)
    date = serializers.DateTimeField(source='create_date',format='%Y-%m-%d %H:%M%S')


    class Meta:
        model = models.Book
        fields = ['id','uname','date','title']


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

    def validate(self, attrs):
        attrs['username'] = filter_username(attrs['username'])
        return attrs

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
    groups = serializers.SerializerMethodField('get_groups')

    def get_groups(self,obj):
        return list(set(obj.permlist.values_list('group__id',flat=True)))

    def validate(self, attrs):
        attrs['name'] = filter_username(attrs['name'])
        return attrs

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



class groupPermSerializer(ModelSerializer):

    class Meta:
        fields = ('id','name','permissions')
        model = Group
        depth = 1

