from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from utils.common import BaseViewSet, ResDict, hander_error
from goods.serializers import GoodsOneSerializer, \
    GoodsBaseSerializer, GoodsCreateSerializer, \
    GoodsInfoSerializer, GoodsTagSerializer, GoodsInfoCreateSerializer, GoodsInfoEditSerializer
from goods.models import *


class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 10


class GoodsList(BaseViewSet):
    queryset = GoodsLevelOne.objects.all()
    serializer_class = GoodsBaseSerializer
    serializer_create = GoodsCreateSerializer

    def list(self, request, *args, **kwargs):
        level = kwargs['pk']
        if level == 1:
            self.serializer_class.Meta.fields = ('id', 'name', 'is_active', 'level')
        elif level == 2:
            self.serializer_class.Meta.fields = \
                ('id', 'name', 'is_active', 'level', 'children')
        elif level == 3:
            self.serializer_class = GoodsOneSerializer

        return super(GoodsList, self).list(request, *args, **kwargs)

    def filter_level(self, level):
        goods_model = {1: GoodsLevelOne, 2: GoodsLevelTwo, 3: GoodsLevelThree}
        model = goods_model.get(level, None)
        self.serializer_create.Meta.model = model

    def create(self, request, *args, **kwargs):
        level = int(request.data.get('level', -1))
        if level not in [1, 2, 3]:
            return Response(ResDict(400, msg='等级参数非法'))

        self.filter_level(level)
        return super(GoodsList, self).create(request,serializer=self.serializer_create)


    def update(self, request, *args, **kwargs):

        level = int(request.data.get('level', -1))
        if level not in [1, 2, 3]:
            return Response(ResDict(400, msg='等级参数非法'))

        self.filter_level(level)
        obj = self.serializer_create.Meta.model.objects.filter(id=kwargs['pk'])
        if obj:
            try:
                obj.update(**request.data)
            except Exception as e:
                return Response(ResDict(400, msg=str(e)))
            return Response(ResDict(200, msg='更新成功'))

        else:
            return Response(ResDict(400, msg='修改分类不存在'))


    def destroy(self, request, *args, **kwargs):

        level = int(request.data.get('level', -1))

        if level not in [1, 2, 3]:
            return Response(ResDict(400, msg='等级参数非法'))

        self.filter_level(level)

        obj = self.serializer_create.Meta.model.objects.filter(id=kwargs['pk']).first()
        if obj:
            obj.delete()
            return Response(ResDict(200, msg='删除成功'))
        else:
            return Response(ResDict(400, msg='分类不存在'))


class GoodsInfoList(BaseViewSet):
    queryset = GoodSInfo.objects.all()
    serializer_class = GoodsInfoSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        cate_id = kwargs['pk']
        queryset = self.get_queryset()
        sel_an = queryset.filter(category_id=cate_id, sel=0)
        sel_static = queryset.filter(category_id=cate_id, sel=1)
        serializer_an = self.serializer_class(sel_an, many=True)
        serializer_static = self.serializer_class(sel_static, many=True)
        resp = {'animate': serializer_an.data,
                'static': serializer_static.data}
        return Response(ResDict(200, data=resp))

    def create(self, request, *args, **kwargs):
        return super(GoodsInfoList, self).create(request,serializer=GoodsInfoCreateSerializer)

    def update(self, request, *args, **kwargs):
        return super(GoodsInfoList, self).update(request,serializer=GoodsInfoEditSerializer)




class GoodsTag(BaseViewSet):
    queryset = GoodsInfoTag.objects.all()
    serializer_class = GoodsTagSerializer
