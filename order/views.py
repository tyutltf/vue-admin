import django_filters
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from utils.common import ResDict,BaseViewSet
from order.models import Order,OrderLogistics
from order.serializers import OrderSerializer,OrderLogisticsSer
import django_filters.rest_framework as filters
# Create your views here.



class filterOrder(django_filters.FilterSet):
    order_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['order_number',]

class OrderView(BaseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = filterOrder



class OrderLogisticsView(BaseViewSet):
    queryset = OrderLogistics.objects.all()
    serializer_class = OrderLogisticsSer


    def retrieve(self, request, *args, **kwargs):
        order_id = kwargs['pk']
        queryset = self.queryset.filter(order_id=order_id)
        serializer = self.serializer_class(queryset,many=True)
        return Response(ResDict(200,data=serializer.data))
