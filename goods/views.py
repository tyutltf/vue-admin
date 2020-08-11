from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from goods.serializers import GoodsOneSerializer
from goods.models import *


class GoodsList(ModelViewSet):
    queryset = GoodsLevelOne.objects.all()
    serializer_class = GoodsOneSerializer


