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

