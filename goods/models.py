from django.db import models


class GoodsLevelOne(models.Model):
    name = models.CharField(max_length=120, verbose_name='分类名称')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    level = models.SmallIntegerField(verbose_name='等级', default=1)

    class Meta:
        verbose_name = verbose_name_plural = '一级分类'

    def __str__(self):
        return self.name


class GoodsLevelTwo(models.Model):
    name = models.CharField(max_length=120, verbose_name='分类名称')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    level = models.SmallIntegerField(verbose_name='等级', default=2)
    father = models.ForeignKey('GoodsLevelOne', verbose_name='上级菜单', on_delete=models.CASCADE, related_name='children')

    class Meta:
        verbose_name = verbose_name_plural = '二级分类'

    def __str__(self):
        return self.name


class GoodsLevelThree(models.Model):
    name = models.CharField(max_length=120, verbose_name='分类名称')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    level = models.SmallIntegerField(verbose_name='等级', default=3)
    father = models.ForeignKey('GoodsLevelTwo', verbose_name='上级菜单',
                               on_delete=models.CASCADE, related_name='children')

    class Meta:
        verbose_name = verbose_name_plural = '三级分类'

    def __str__(self):
        return self.name


class GoodSInfo(models.Model):
    name = models.CharField(max_length=300, verbose_name='分类参数名称')
    category = models.ForeignKey(GoodsLevelThree, verbose_name='所属分类',
                                 on_delete=models.CASCADE, related_name='category')
    sel = models.SmallIntegerField(verbose_name='类别')
    create_date = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '商品参数'
        ordering = ['-create_date']

    def __str__(self):
        return self.name


class GoodsInfoTag(models.Model):

    name = models.CharField(max_length=120,verbose_name='标签名称')
    goodsInfo = models.ForeignKey('GoodSInfo',on_delete=models.CASCADE,
                                  related_name='tag',verbose_name='分类标签')
    create_date = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '参数标签'
        ordering = ['-create_date']

    def __str__(self):
        return self.name


class GoodsProductList(models.Model):

    choices = (
        (0,'未通过'),
        (1,'审核中'),
        (2, '已审核'),
    )
    goods_name = models.CharField(max_length=640,verbose_name='商品名称',unique=True)
    goods_price = models.DecimalField(max_digits=15,decimal_places=4,verbose_name='商品价格')
    goods_number = models.IntegerField(verbose_name='商品数量',default=0)
    goods_weight = models.CharField(max_length=120,verbose_name='商品重量',)
    goods_state = models.SmallIntegerField(verbose_name='商品状态',choices=choices,default=0)
    goods_animate = models.JSONField(verbose_name='动态信息',null=True,blank=True)
    goods_static = models.JSONField(verbose_name='静态信息',null=True,blank=True)
    goods_content = models.TextField(verbose_name='商品内容',null=True,blank=True)
    goods_image = models.ManyToManyField('GoodsImage',verbose_name='商品图片',blank=True,null=True)
    goods_cate = models.ForeignKey('GoodsLevelThree',on_delete=models.CASCADE,
                                   null=True,blank=True,verbose_name='商品分类')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    up_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    hot_mumber = models.IntegerField(verbose_name='热销品数量',default=0)
    is_promote = models.BooleanField(verbose_name='是否是热销品',default=0)

    class Meta:
        verbose_name = verbose_name_plural = '商品列表'
        ordering = ['-up_time']

    def __str__(self):
        return self.goods_name



class GoodsImage(models.Model):
    goods = models.ForeignKey(GoodsProductList, verbose_name='对应商品',
                              on_delete=models.CASCADE, related_name='goods', null=True, blank=True)

    image = models.ImageField(upload_to='image/',verbose_name='图片文件')

    def __str__(self):
        return self.image.name
    class Meta:
        verbose_name = verbose_name_plural = '商品图片'









