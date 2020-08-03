from rest_framework import serializers
from datetime import date
from rest_framework.serializers import ModelSerializer
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

    groups = serializers.SerializerMethodField('get_group')

    def get_group(self,obj):
        return obj.groups.first().name

    class Meta:
        fields = ('id','username','email','telephone','groups','is_active')
        model = models.User


class MenuChildSerialiser(ModelSerializer):

    class Meta:
        fields = ('id', 'name','url')
        model = models.MenuChild

class MenuSerialiser(ModelSerializer):

    # children = serializers.SerializerMethodField('get_child')
    # def get_child(self,obj):
    #     return MenuChildSerialiser(instance=obj).data
    children = MenuChildSerialiser(many=True,read_only=True)

    class Meta:
        fields = ('id','name','children')
        model = models.Menu
        depth = 1
