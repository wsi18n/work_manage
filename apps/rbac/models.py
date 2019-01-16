from django.db import models

from work_manage.admin import base

# Create your models here.
class Menu(base.Model):
    name = models.CharField(max_length=32, verbose_name='名称',unique=True)
    url = models.CharField(max_length=128, verbose_name='权限url', null=True, blank=True ,default=None)
    parent = models.ForeignKey("self",on_delete=models.SET_NULL, null=True, blank=True, verbose_name="父菜单")

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Role(base.Model):

    name = models.CharField(max_length=20, verbose_name='角色名称')
    permission = models.ManyToManyField(Menu, verbose_name='权限',blank=True)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
