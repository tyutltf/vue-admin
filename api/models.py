from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=300,verbose_name='图书',unique=True)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = '图书'

class User(AbstractUser):
    telephone = models.CharField(max_length=20,verbose_name='手机号',default='18550774645')
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = verbose_name_plural = '用户'

class Menu(models.Model):

    name = models.CharField(max_length=120,verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class Meta:
        verbose_name = verbose_name_plural = '一级菜单'

    def __str__(self):
        return self.name


class MenuChild(models.Model):
    name = models.CharField(max_length=120, verbose_name='名称')
    menu = models.ForeignKey('menu',verbose_name='上级菜单',on_delete=models.CASCADE,related_name='children')
    url = models.CharField(max_length=120,verbose_name='路由',default='')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '二级菜单'

    def __str__(self):
        return self.name
