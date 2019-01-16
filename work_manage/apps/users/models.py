from django.db import models
from work_manage.admin import base

from rbac.models import Role
from django.contrib.auth.models import AbstractBaseUser


class Department(base.Model):
    name = models.CharField(max_length=20, verbose_name='部门名字', unique=True, )
    parent = models.ForeignKey("self", on_delete=models.SET_NULL,related_name='sub_departments',
                               verbose_name='父级组织', blank=True,
                               null=True)

    def all_sub_departments(self):
        sub_dps = self.sub_departments.all()
        for sub_dp in sub_dps:
            sub_dps = sub_dps | sub_dp.all_sub_departments()
        return sub_dps
    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(base.Model):
    name = models.CharField(max_length=20, verbose_name="岗位名称")
    # 默认是普通员工
    is_leader = models.BooleanField(default=False, verbose_name="岗位类别")
    def __str__(self):
        return self.name


class UserProfile(AbstractBaseUser,base.Model):
    GENDER = (("male", "男"), ("female", "女"))
    username = models.CharField(max_length=20, verbose_name="用户名", unique=True, db_index = True)
    alias = models.CharField(max_length=20, verbose_name="姓名", blank=True, null=True)
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['name']
    # password = models.CharField(max_length=32, verbose_name="密码")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    gender = models.CharField(max_length=10,
                              choices=GENDER,
                              default="male",
                              verbose_name="性别")
    mobile = models.CharField(max_length=11, default="", verbose_name="电话",
                              blank=True, null=True)
    email = models.EmailField(max_length=100, verbose_name="邮箱", blank=True,
                              null=True)
    department = models.ForeignKey(Department, to_field="name", null=True,
                                   blank=True,
                                   on_delete=models.CASCADE,
                                   verbose_name="部门",
                                   related_name='users_set')
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="职位")
    roles = models.ManyToManyField(Role, verbose_name="角色",
                                   related_name="users_set")
    joined_date = models.DateField(null=True, blank=True, verbose_name="入职日期")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        if self.alias :
            return self.alias +" "+ self.username
        return self.username
