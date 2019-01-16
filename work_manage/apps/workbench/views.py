from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q

from rbac import models as rbac_m
from users import models as users_m
from users.models import UserProfile
from workbench import models as workbench_m

from work_manage.admin.base import View as _View

#from django.views.generic.base import View
import time
import os
import logging
logger = logging.getLogger(__name__)
# logger.error("")


class View(_View):
    @classmethod
    def render(cls,request, template, context={}, *args, **kwargs):
        context.update({
            'msg_count':request.user.message_set.filter(state=1).count()
        })
        return super(View, cls).render(request, template, context, *args, **kwargs)


# Create your views here.
def index(request):
    return View.render(request, 'workbench/index.html')

@require_POST
def upload(request):
    file_from = request.GET.get('from')
    file_type = request.GET.get('type')
    try:
        path = os.path.join('static', 'upload', file_from)
        if not os.path.exists(path):
            os.makedirs(path)
        f = request.FILES["upload"]
        file_name = os.path.join(path, time.strftime("%Y%m%d%H%M%S", time.localtime()) + f.name)
        des_origin_f = open(file_name, "wb+")
        for chunk in f.chunks():
            des_origin_f.write(chunk)
        des_origin_f.close()
        return JsonResponse({
            "uploaded": 1,
            "fileName": f.name,
            "url": '/' + file_name
        })
    except Exception as e:
        print(e)

    return JsonResponse({
        "uploaded": 0,
        "error": {
            "message": "upload filed"
        }
    })

class UserConfig(View):
    @classmethod
    def get(cls, request):
        return cls.render(request, 'workbench/user_config.html')
        #return _render(request, 'workbench/user_config.html')

    @classmethod
    def post(cls, request):
        user = request.user

        if all((request.POST.get('old_pwd'),request.POST.get('new_pwd'),request.POST.get('re_pwd'))):
            if request.POST['old_pwd'] == user.password:
                if len(request.POST['new_pwd']) >= 6:
                    if request.POST['new_pwd'] == request.POST['re_pwd']:
                        user.password = request.POST['new_pwd']
                        user.save()
                        messages.success(request, '修改密码成功')
                        return cls.get(request)
                    else:
                        messages.error(request, '保存失败:重复密码不一致')
                        return cls.get(request)
                else:
                    messages.error(request, '保存失败:密码需6位以上')
                    return cls.get(request)
            else:
                messages.error(request, '保存失败:原密码错误')
                return cls.get(request)
        elif any((request.POST.get('old_pwd'),request.POST.get('new_pwd'),request.POST.get('re_pwd'))):
            messages.error(request, '保存失败:表单未填写完整')
            return cls.get(request)


        if request.POST.get('name'):
            user.name = request.POST['name']
        if request.POST.get('gender'):
            user.gender = request.POST['gender']
        if request.POST.get('birthday'):
            user.birthday = request.POST['birthday']
        if request.POST.get('e-mail'):
            user.email = request.POST['e-mail']
        if request.POST.get('mobile'):
            user.mobile = request.POST['mobile']
        user.save()
        messages.success(request, '保存成功')
        return cls.get(request)


class MessageView(View):

    @classmethod
    def get(cls, request):
        msg_list = request.user.message_set.filter(state=1).order_by('-id')
        return cls.render(request, 'workbench/message.html',{'msg_list' : msg_list})

    @classmethod
    def post(cls, request):
        id = request.POST.get('id')
        msg_obj = get_object_or_404(workbench_m.Message, pk=id)
        msg_obj.state = 2 #已确认
        msg_obj.received_describe = request.POST.get('describe')
        msg_obj.received_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        msg_obj.save()

        messages.success(request, '消息确认')
        return cls.get(request)


class PlanView:
    #根据判断部门和职位判断是否有权限
    @staticmethod
    def judge_privilege_with_post(user,plan,method='view'):
        if method == 'view':
            if user in plan.related_user.all():
                return True

            if user == plan.head or user == plan.creator:
                return True

            if user.post and user.post.is_leader:#如果是领导
                depart_list = list(user.department.all_sub_departments())  # 递归获取所有子部门
                depart_list.append(user.department)#管理的所有部门

                related_users = list(plan.related_user.all())
                related_users.extend([plan.creator, plan.head])

                #任务相关人员所在的部门
                depart_list2 = list(users_m.Department.objects.filter(users_set__in=related_users).distinct())

                if set(depart_list).intersection(set(depart_list2)):#交集，交集不为空说明有权查看
                    return True
        if method == 'edit':
            if user == plan.creator:
                return True
        if method == 'delete':
            if user == plan.creator:
                return True
        return False
    @staticmethod
    def get_q(user,sw):#获得plan_list过滤器，根据判断部门和职位

        if sw =='my':#查看自己相关的任务
            return Q(creator=user) | Q(head=user) | Q(related_user=user)


        depart_list = list(user.department.all_sub_departments())  # 递归获取所有子部门
        depart_list.append(user.department)

        department_users = list(UserProfile.objects.filter(department__in=depart_list))

        if sw == 'staff':#查看部门员工相关的任务
            department_users.remove(user)  # 部门下，除我以外的所有user
            if user.post and user.post.is_leader:
                return Q(creator__in=department_users) | Q(head__in=department_users) | Q(related_user__in=department_users)
            else:
                return None

        if sw == 'auto':
            if user.post and user.post.is_leader:#如果是领导,所有员工相关的任务
                return Q(creator__in=department_users) | Q(head__in=department_users) | Q(related_user__in=department_users)
            else :#如果不是领导,自己的任务
                return Q(creator=user) | Q(head=user) | Q(related_user=user)

    class Delete(View):
        @classmethod
        def get(cls, request, id):
            user = request.user
            plan = get_object_or_404(workbench_m.Plan, pk=id)
            if not PlanView.judge_privilege_with_post(user,plan,'delete'):
                messages.error(request, '你不能删除该任务')
                return cls.render403(request)

            plan.disable()
            return JsonResponse({'status':1,'msg':'删除成功'})

    class Detail(View):
        @classmethod
        def get(cls, request, id):
            user = request.user
            plan = get_object_or_404(workbench_m.Plan, pk=id)
            if not PlanView.judge_privilege_with_post(user,plan):
                messages.error(request, '你已不能查看该任务')
                return cls.render403(request)
            q=PlanView.get_q(user,'auto')

            sub_plan_list = workbench_m.Plan.objects.filter(q,parent=plan).order_by('id')

            return cls.render(request, 'workbench/plan_detail.html', {
                'plan': plan,
                'all_plan_state': workbench_m.Plan.STATE,
                'sub_plan_list': sub_plan_list
            })
        @classmethod
        def post(cls, request, id):
            plan = get_object_or_404(workbench_m.Plan, pk=id)
            plan.state = request.POST.get('state')
            if plan.state == '3':  # 已完成
                plan.completion_date = time.strftime('%Y-%m-%d', time.localtime())
                plan.close_sub_plan()  # 关闭子计划
            plan.save()

            messages.success(request, '任务状态更新成功')
            return cls.get(request,id)

    class New(View):
        @classmethod
        def get(cls,request,parent_id):

            # 所有的user用来生成<select>的<option>
            all_users = UserProfile.objects.all()
            all_plan_type = workbench_m.PlanType.objects.all()
            context = {
                'all_plan_state': workbench_m.Plan.STATE,
                'all_users': all_users,
                'all_plan_type':all_plan_type
            }
            return cls.render(request, 'workbench/plan_new.html', context)
        @classmethod
        def post(cls,request, parent_id):
            plan = workbench_m.Plan()
            plan.name = request.POST['name']
            plan.head = UserProfile.objects.get(id=request.POST['head'])#leader
            plan.plan_type = workbench_m.PlanType.objects.get(pk=request.POST['type'])
            plan.state = request.POST['state']
            if request.POST['planned_completion_date']:
                plan.planned_completion_date = request.POST['planned_completion_date']
            if parent_id:
                plan.parent = workbench_m.Plan(id = parent_id)
            plan.description = request.POST['description']

            plan.creator = request.user
            plan.pub_date = time.strftime('%Y-%m-%d',time.localtime())

            plan.save()
            plan.related_user.add(*request.POST.getlist('related_user[]'))
            plan.save()

            if request.FILES.get('file'):
                attach = workbench_m.Attachment(file=request.FILES['file'], plan=plan)
                attach.save()

                # 创建Message 通知相关user
            for user in plan.related_user.all():
                workbench_m.Message.new_message(plan, user, "你参与到了'%s'的任务中，该任务负责人是'%s'" % (plan.name, plan.head))
            workbench_m.Message.new_message(plan, plan.head, "你参与到了'%s'的任务中，并负责该任务" % plan.name)

            messages.success(request, '保存成功')
            return cls.get(request,parent_id)

    class Edit(View):
        @classmethod
        def get(cls,request, id):
            plan = get_object_or_404(workbench_m.Plan, pk=id)

            # 所有的user用来生成<select>的<option>
            all_users = UserProfile.objects.all()
            all_plan_type = workbench_m.PlanType.objects.all()

            # 相关的user_id用来生成<option selected>
            related_users_ids = []
            for row in plan.related_user.all():
                related_users_ids.append(row.id)

            context = {
                'plan': plan,
                'all_plan_state': workbench_m.Plan.STATE,
                'all_users': all_users,
                'all_plan_type':all_plan_type,
                'related_users_ids':related_users_ids,
             }
            return cls.render(request, 'workbench/plan_edit.html', context )

        @classmethod
        def post(cls,request, id):
            user =request.user
            plan = get_object_or_404(workbench_m.Plan, pk=id)
            if not PlanView.judge_privilege_with_post(user,plan,'edit'):
                messages.error(request, '你不能编辑该任务')
                return cls.render403(request)

            plan.name = request.POST['name']
            if request.POST.get('head'):
                plan.head = UserProfile.objects.get(id=request.POST['head'])
            if request.POST.get('description'):
                plan.description = request.POST['description']
            if request.POST.get('planned_completion_date'):
                plan.planned_completion_date = request.POST['planned_completion_date']
            if request.POST.get('type'):
                plan.plan_type = workbench_m.PlanType.objects.get(pk=request.POST['type'])
            if request.POST.get('state'):
                plan.state = request.POST['state']
                if plan.state == '3':#已完成
                    plan.completion_date = time.strftime('%Y-%m-%d', time.localtime())
                    plan.close_sub_plan()#关闭子计划


            if request.POST.get('related_user[]'):
                related_users = request.POST.getlist('related_user[]') #[1,3,...]
                plan.related_user.clear()
                plan.related_user.add(*related_users)

            plan.save()

            if request.FILES.get('file'):
                attach = workbench_m.Attachment(file=request.FILES['file'], plan=plan)
                attach.save()

            messages.success(request, '保存成功')
            return cls.get(request, id)



    class List(View):
        @staticmethod
        def get_filter_params(request):
            filter_params = {}
            if request.GET.get('all'):
                filter_params.update({'parent__isnull': True})
            if request.GET.get('name'):
                filter_params.update({'name__contains': request.GET['name']})
            if request.GET.get('creator'):
                filter_params.update({'creator_id': request.GET['creator']})
            if request.GET.get('state'):
                filter_params.update({'state': request.GET['state']})
            if request.GET.get('type'):
                filter_params.update({'plan_type': request.GET['type']})
            if request.GET.get('head'):
                filter_params.update({'head_id': request.GET['head']})
            if request.GET.get('dp'):
                filter_params.update({'head_id': request.GET['dp']})
            if request.GET.get('start_time'):
                filter_params.update({'planned_completion_date__gte': request.GET['start_time']})
            if request.GET.get('end_time'):
                filter_params.update({'pub_date__lte': request.GET['end_time']})
            return filter_params

        @classmethod
        def get(cls, request, staff_plan):
            user = request.user
            filter_params = cls.get_filter_params(request)
            plan_list = []

            if staff_plan:# 部门员工相关的任务
                q = PlanView.get_q(user,'staff')
                if q:
                    plan_list = workbench_m.Plan.objects.filter(q, **filter_params).distinct()
                else:
                    messages.error(request, '不能查看部门其他职员的工作任务')

            else:# 我相关的任务
                q = PlanView.get_q(user,'my')
                plan_list = workbench_m.Plan.objects.filter(q,**filter_params).distinct()
            #for i in range(len(plan_list)):
            #    plan = plan_list[i]
            #    related_users = list(plan.related_user.all())
            #    related_users.append(plan.head)
            #    plan_list[i].depart_list = users_m.Department.objects.filter(users_set__in=related_users).distinct()

            return cls.render(request, 'workbench/plan_list.html', {
                'plan_list': plan_list,
                'all_users': UserProfile.objects.all(),
                'all_plan_state': workbench_m.Plan.STATE,
                'all_plan_type': workbench_m.PlanType.objects.all()

            })

    class Overview(View):
        @classmethod
        def get(cls,request):
            return cls.render(request, 'workbench/plan_overview.html')


class Doc(View):
    @classmethod
    def get(cls,request):
        return cls.render(request, 'workbench/index.html')
