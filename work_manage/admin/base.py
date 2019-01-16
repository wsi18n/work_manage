from django.views.generic.base import View as _View
from django.db import models
from .tools import MyLoginRequest


class View(MyLoginRequest,_View):
    @classmethod
    def render(cls, request, template, *args, **kwargs):
        from .tools import render #函数内import 避免循环import报错
        return render(request, template, *args, **kwargs)

    @classmethod
    def render404(cls, request, *args, **kwargs):
        return cls.render(request, 'page404.html', status=404, *args, **kwargs)

    @classmethod
    def render403(cls, request, *args, **kwargs):
        return cls.render(request, 'page403.html', status=403, *args, **kwargs)


class Manager(models.Manager):
    def filter(self, *args, **kwargs):
        if not 'is_able' in kwargs.keys():  # 如果需要查看所有数据，
            kwargs['is_able'] = True
        return super().filter(*args, **kwargs)

    def exclude(self,*args, **kwargs):
        if not 'is_able' in kwargs.keys():
            kwargs['is_able'] = False
        return super().exclude(*args, **kwargs)

    def all(self):
        return self.filter()

    def count(self):
        return self.filter().count()

    def get(self, *args, **kwargs):
        return self.filter().get(*args, **kwargs)

class Model(models.Model):
    is_able = models.BooleanField(default=True, verbose_name='是否启用')

    objects = Manager()

    def disable(self):
        self.is_able =False
        self.save(update_fields=['is_able'])

    class Meta:
        abstract = True #设置为 True, django 不会将这个通用Model 写入数据库

