from django.contrib import admin
from goods.models import *

# Register your models here.
class showGoodsLevelOne(admin.ModelAdmin):
    list_display = ('id','name','level','is_active')
    list_editable = ('name','level','is_active')

class showGoodsLevelTwo(admin.ModelAdmin):
    list_display = ('id','name','level','is_active','GoodsLevelOne')
    list_editable = ('name','level','is_active','GoodsLevelOne')

class showGoodsLevelThree(admin.ModelAdmin):
    list_display = ('id','name','level','is_active','GoodsLevelTwo')
    list_editable = ('name','level','is_active','GoodsLevelTwo')

admin.site.register(GoodsLevelOne,showGoodsLevelOne)
admin.site.register(GoodsLevelTwo,showGoodsLevelTwo)
admin.site.register(GoodsLevelThree,showGoodsLevelThree)

