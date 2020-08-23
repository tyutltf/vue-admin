from django.contrib import admin

# Register your models here.
from order.models import Order,OrderLogistics


class showOrder(admin.ModelAdmin):
    list_display = ('id','order_number','order_price','order_pay',\
                    'is_send','create_time','up_time')
    list_editable = ('order_number','order_price','order_pay',\
                    'is_send')

class showOrderLogistics(admin.ModelAdmin):
    list_display = ('id','content','order')
    list_editable = ('content','order')


admin.site.register(Order,showOrder)
admin.site.register(OrderLogistics,showOrderLogistics)