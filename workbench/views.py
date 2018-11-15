from django.shortcuts import render, reverse, get_object_or_404
from rbac.models import Menu
from . import models
from work_manage.admin.base import View
import logging
logger = logging.getLogger(__name__)
#logger.error("")

def _render(request, template, context={}):
    context.update({
        'top_menu': Menu.objects.filter(parent__isnull=True).values('name', 'url'),
        'left_menu': {
            '个人中心': reverse('workbench:UserConfig'),
            '我的消息': reverse('workbench:Message'),
            '工作计划': {
                '计划总览': reverse('workbench:Plan.Overview'),
                '创建的计划': reverse('workbench:Plan.Created'),
                '收到的计划': reverse('workbench:Plan.Received'),
                '审批的计划': reverse('workbench:Plan.Examine'),
            },
            '我的文档': reverse('workbench:Doc'),
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


class Message(View):
    @staticmethod
    def get(request):
        return _render(request, 'workbench/index.html')


class Plan:
    class Detail(View):
        @staticmethod
        def get(request,id):
            plan = get_object_or_404(models.Plan, pk= id)
            sub_plan_list = models.Plan.objects.filter(parent=plan).order_by('id')

            return _render(request, 'workbench/created_plan_detail.html',{'plan':plan,'sub_plan_list':sub_plan_list})


    class Created(View):
        @staticmethod
        def get(request):
            plan_list = models.Plan.objects.filter(creator=request.user,parent__isnull=True).order_by('id')
            return _render(request, 'workbench/created_plan_list.html',{'plan_list':plan_list})
    class Examine(View):
        @staticmethod
        def get(request):
            return _render(request, 'workbench/index.html')
    class Received(View):
        @staticmethod
        def get(request):
            return _render(request, 'workbench/index.html')


    class Overview(View):
        @staticmethod
        def get(request):
            return _render(request, 'workbench/index.html')


class Doc(View):
    @staticmethod
    def get(request):
        return _render(request, 'workbench/index.html')
