from django.db import models
from django.contrib.auth.models import AbstractUser
from rbac.models import Role


class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name='部门名字',unique=True)
    leader = models.CharField(max_length=20, verbose_name='部门领导',unique=True)
    parent = models.ForeignKey("self",on_delete=models.SET_NULL,verbose_name='父级组织',blank=True,null=True)
    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s' %(self.name,self.leader)


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")),
                              default="male",
                              verbose_name="性别")
    mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    email = models.EmailField(max_length=100, verbose_name="邮箱")
    department = models.ForeignKey(Department, to_field="name", null=True, blank=True,on_delete=models.CASCADE,
                                   verbose_name="部门",related_name='部门')
    post = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey(Department, to_field="leader", null=True, blank=True,on_delete=models.CASCADE,
                                 verbose_name="上级主管", related_name='上级主管')
    roles = models.ManyToManyField(Role, verbose_name="角色",related_name="role")
    joined_date = models.DateField(null=True, blank=True, verbose_name="入职日期")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
