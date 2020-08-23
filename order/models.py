from django.db import models

# Create your models here.


class Order(models.Model):

    order_number = models.CharField(max_length=120,verbose_name='订单编号',unique=True)
    order_price = models.DecimalField(max_digits=15,decimal_places=4,verbose_name='订单价格')
    order_pay = models.BooleanField(verbose_name='是否付款',default=False)
    is_send = models.BooleanField(verbose_name='是否发货',default=False)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    up_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    goods = models.ManyToManyField('goods.GoodsProductList',verbose_name='商品列表',null=True,blank=True)


    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = verbose_name_plural = '订单'



class OrderLogistics(models.Model):

    content = models.CharField(max_length=1200,verbose_name='物流信息')
    ftime = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    order = models.ForeignKey('order',verbose_name='订单',related_name='order',
                              on_delete=models.CASCADE)
    class Meta:
        verbose_name = verbose_name_plural = '订单物流'
