from django.db import models
from work_manage.admin.base import Model
from users.models import UserProfile
# Create your models here.
from work_manage.settings import STATIC_URL
import time

class PlanType(Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    def __str__(self):
        return self.name

class Plan(Model):
    STATE = (
        ('1', '进行中'),
        ('2', '挂起'),
        ('3', '已完成'),
    )
    name = models.CharField(max_length=32, verbose_name='名称')
    creator = models.ForeignKey(UserProfile, related_name="created_plan", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="创建者")
    head = models.ForeignKey(UserProfile, related_name="led_plan", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="负责人")
    #approver = models.ForeignKey(UserProfile, related_name="approval_plan", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="审批者")
    related_user = models.ManyToManyField(UserProfile, related_name="related_plan", blank=True, verbose_name='相关人员')
    state = models.CharField(max_length=10, default="2", choices=STATE, verbose_name='计划状态')
    description = models.TextField(default='', blank=True, verbose_name='计划描述')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='父计划')
    complete_percent = models.PositiveSmallIntegerField(default=0, verbose_name="完成百分比"),
    pub_date =  models.DateField(null=True, blank=True, verbose_name="发布日期")
    completion_date =  models.DateField(null=True, blank=True, verbose_name="完成日期")
    planned_completion_date =  models.DateField(null=True, blank=True, verbose_name="预计完成日期")
    update_time = models.DateTimeField(auto_now=True, editable=False, verbose_name='更新时间')
    img_url = models.URLField(null=True, verbose_name='图片URL')
    plan_type = models.ForeignKey(PlanType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='任务类型')

    #递归关闭所有子计划(设置state=已完成 & 设置完成时间)
    def close_sub_plan(self):
        sub_plan_list = self.plan_set.exclude(state=3)
        for sub_plan in sub_plan_list:
            sub_plan.close_sub_plan()
        # .update()以后queryset对象会删除？，所以for循环要在update之前
        sub_plan_list.update(state=3, completion_date=time.strftime('%Y-%m-%d', time.localtime()))

    class Meta:
        verbose_name = '工作计划'

    def __str__(self):
        return self.name

def get_file_path(instance, filename):
    return '%s/upload/plan_%s/%s' % (STATIC_URL.strip('/'), instance.plan.id, filename)

class Attachment(Model):
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属plan')
    file = models.FileField(upload_to=get_file_path, verbose_name="附件", blank=True, null=True)
    update_time = models.DateTimeField(auto_now=True, editable=False, verbose_name='更新时间')


class Message(Model):
    STATE=(
        ('1', '未确认'),
        ('2', '已确认'),
        ('3', '推迟'),
    )
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='相关plan')
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='相关用户')
    content = models.CharField(max_length=256, blank=True, null=True, verbose_name="消息内容")
    state = models.CharField(max_length=4, default="1", choices=STATE, verbose_name='消息状态')
    pub_time = models.DateTimeField( verbose_name='出现时间')
    received_time = models.DateTimeField(null=True, blank=True, verbose_name='确认时间')
    received_describe = models.CharField(max_length=256, blank=True, null=True, verbose_name="确认描述")

    @staticmethod
    def new_message(plan, user, content=''):
        msg_obj = Message()
        msg_obj.plan = plan
        msg_obj.user = user
        msg_obj.content = content
        msg_obj.pub_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        msg_obj.save()
        return msg_obj





