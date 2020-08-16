from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from goods.models import *


class GoodsTwoSerializer(ModelSerializer):

    class Meta:
        fields = ('id','name','is_active','level','children')
        model = GoodsLevelTwo
        depth = 1



class GoodsOneSerializer(ModelSerializer):

    children = GoodsTwoSerializer(many=True,read_only=True)

    class Meta:
        fields = ('id','name','is_active','level','children')
        model = GoodsLevelOne

class GoodsBaseSerializer(ModelSerializer):

    class Meta:
        fields = ('id','name','is_active','level','children')
        model = GoodsLevelOne
        depth = 1

class GoodsCreateSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = GoodsLevelOne


class GoodsInfoSerializer(ModelSerializer):


    class Meta:
        fields = ('id','name','sel','category_id','tag')
        model = GoodSInfo
        depth = 1

class GoodsInfoCreateSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = GoodSInfo

class GoodsInfoEditSerializer(ModelSerializer):

    class Meta:
        fields = ('name',)
        model = GoodSInfo

class GoodsTagSerializer(ModelSerializer):
    class Meta:
        model = GoodsInfoTag
        fields = '__all__'