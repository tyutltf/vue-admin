from django.db import models


class GoodsLevelOne(models.Model):

    name = models.CharField(max_length=120, verbose_name='分类名称')
    is_active = models.BooleanField(default=True,verbose_name='是否激活')
    level = models.SmallIntegerField(verbose_name='等级',default=1)

    class Meta:
        verbose_name = verbose_name_plural = '一级分类'

    def __str__(self):
        return self.name


class GoodsLevelTwo(models.Model):
    name = models.CharField(max_length=120, verbose_name='分类名称')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    level = models.SmallIntegerField(verbose_name='等级',default=2)
    GoodsLevelOne = models.ForeignKey('GoodsLevelOne',verbose_name='上级菜单',on_delete=models.CASCADE,related_name='children')


    class Meta:
        verbose_name = verbose_name_plural = '二级分类'

    def __str__(self):
        return self.name


class GoodsLevelThree(models.Model):
    name = models.CharField(max_length=120, verbose_name='分类名称')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    level = models.SmallIntegerField(verbose_name='等级',default=3)
    GoodsLevelTwo = models.ForeignKey('GoodsLevelTwo',verbose_name='上级菜单',
                                      on_delete=models.CASCADE,related_name='children')

    class Meta:
        verbose_name = verbose_name_plural = '三级分类'

    def __str__(self):
        return self.name