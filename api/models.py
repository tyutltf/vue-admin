from django.db import models
from django.contrib.auth.models import AbstractUser, Group,Permission


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=300,verbose_name='图书',unique=True)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = '图书'


class RolePermlist(models.Model):
    group = models.SmallIntegerField(verbose_name='组id',null=True,blank=True)
    permissions = models.ManyToManyField(Permission,verbose_name='权限列表',null=True,blank=True)


    class Meta:
        verbose_name = verbose_name_plural = '角色'

class Role(models.Model):

    name = models.CharField(max_length=120,verbose_name='角色名',default='管理员',unique=True)
    info = models.CharField(max_length=600,verbose_name='角色描述',default='')
    permlist = models.ManyToManyField(Permission,verbose_name='权限列表',null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '角色'
        ordering= ['-create_date']


class User(AbstractUser):
    telephone = models.CharField(max_length=20,verbose_name='手机号',default='18550774645')
    role = models.ForeignKey('role',on_delete=models.CASCADE,verbose_name='用户角色',blank=True,null=True)
    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-date_joined']
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

