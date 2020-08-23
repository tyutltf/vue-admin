from django.contrib import admin
from goods.models import *

# Register your models here.
class showGoodsLevelOne(admin.ModelAdmin):
    list_display = ('id','name','level','is_active')
    list_editable = ('name','level','is_active')

class showGoodsLevelTwo(admin.ModelAdmin):
    list_display = ('id','name','level','is_active','father')
    list_editable = ('name','level','is_active','father')

class showGoodsLevelThree(admin.ModelAdmin):
    list_display = ('id','name','level','is_active','father')
    list_editable = ('name','level','is_active','father')

class showGoodsInfo(admin.ModelAdmin):
    list_display = ('id','name','sel','category','create_date')
    list_editable = ('name','sel','category')

class showGoodsInfoTag(admin.ModelAdmin):
    list_display = ('id','name','goodsInfo')
    list_editable = ('name','goodsInfo')

class showGoodsList(admin.ModelAdmin):
    list_display = ('id' ,'goods_name','goods_price','goods_number','goods_weight','goods_state',
                     'hot_mumber','is_promote')
    list_editable = ('goods_name','goods_price','goods_number','goods_weight','goods_state',
                     'hot_mumber','is_promote')
    list_per_page = 12


admin.site.register(GoodsImage)
admin.site.register(GoodsLevelOne,showGoodsLevelOne)
admin.site.register(GoodsLevelTwo,showGoodsLevelTwo)
admin.site.register(GoodsLevelThree,showGoodsLevelThree)
admin.site.register(GoodSInfo,showGoodsInfo)
admin.site.register(GoodsInfoTag,showGoodsInfoTag)
admin.site.register(GoodsProductList,showGoodsList)

