from django.db import models
from users.models import UserProfile
# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    creator = models.ForeignKey(UserProfile, related_name="created_plan", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="创建者")
    related_user = models.ManyToManyField(UserProfile, related_name="related_plan", blank=True, verbose_name='相关人员')
    description = models.TextField(default='', blank=True, verbose_name='计划描述')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='父计划')
    complete_percent = models.PositiveSmallIntegerField(default=0, verbose_name="完成百分比"),
    pub_date =  models.DateField(null=True, blank=True, verbose_name="发布日期")
    completion_date =  models.DateField(null=True, blank=True, verbose_name="完成日期")
    planned_completion_date =  models.DateField(null=True, blank=True, verbose_name="预计完成日期")
    update_Time = models.DateTimeField(auto_now=True, editable=False, verbose_name='更新时间')
    img_url = models.URLField(null=True, verbose_name='图片URL')

    class Meta:
        verbose_name = '工作计划'

    def __str__(self):
        return self.name
