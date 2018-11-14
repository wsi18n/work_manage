from django.shortcuts import render, reverse
from rbac import models
from work_manage.admin.base import View
import logging
logger = logging.getLogger(__name__)

def _render(request, template, context={}):
    context.update({
        'top_menu': models.Menu.objects.filter(parent__isnull=True).values('name', 'url'),
        'left_menu': {
            '个人中心': reverse('workbench:user_config'),
            '我的消息': reverse('workbench:message'),
            '工作计划': {
                '计划总览': reverse('workbench:Order.overview'),
                '我创建的计划': reverse('workbench:Order.created'),
                '我收到的计划': reverse('workbench:Order.received'),
                '我审批的计划': reverse('workbench:Order.examine'),
            },
            '我的文档': reverse('workbench:doc'),
        }
    })
    return render(request, template, context)


# Create your views here.
def index(request):
    return _render(request, 'workbench/index.html')


class UserConfig(View):
    @staticmethod
    def get(request):
        return _render(request, 'workbench/user_config.html')

    @staticmethod
    def post(request):
        user = request.user
        if request.POST['name']:
            user.name =  request.POST['name']
        user.gender =  request.POST['gender']
        if request.POST['birthday']:
            user.birthday = request.POST['birthday']
        user.email =  request.POST['e-mail']
        user.mobile =  request.POST['mobile']
        user.save()
        return _render(request, 'workbench/user_config.html',{'msg':"保存成功"})


def message(request):
    return _render(request, 'workbench/index.html')


class Order:
    @classmethod
    def created(cls, request):
        return _render(request, 'workbench/index.html')

    @classmethod
    def received(cls, request):
        return _render(request, 'workbench/index.html')

    @classmethod
    def examine(cls, request):
        return _render(request, 'workbench/index.html')

    @classmethod
    def overview(cls, request):
        return _render(request, 'workbench/index.html')


def doc(request):
    return _render(request, 'workbench/index.html')
