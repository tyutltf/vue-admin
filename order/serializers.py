from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from order.models import OrderLogistics,Order



class OrderSerializer(ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    up_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Order
        fields = ('id','order_number','order_price','order_pay','is_send',
                  'create_time','up_time')

class OrderLogisticsSer(ModelSerializer):

    ftime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = OrderLogistics
        fields = ('content','ftime','order_id')
        ordering = ['-create_time']