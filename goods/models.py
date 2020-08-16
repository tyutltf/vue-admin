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
















