from django.urls import path
from .views import *
from . import views as rbacview

app_name = 'rbac'

urlpatterns = [
    # 系统设置首页
    path('', rbacview.index, name="index"),

    # 权限操作URL
    path('menu/display/', MenuView.as_view(), name="menu-display"),
    path('menu/add/', MenuAdd.as_view(), name='menu-add'),
    path('menu/del/', MenuDelete.as_view(), name='menu-delete'),

    # 角色操作URL
    path('role/display/', RoleView.List.as_view(), name='role-display'),
    path('role/<int:id>/edit/', RoleView.Edit.as_view(), name='role-edit'),
    path('role/add/', RoleView.Add.as_view(), name='role-add'),
    path('role/del/', RoleView.Delete.as_view(), name='role-delete'),

    # 组织架构
    path('department/display/', DepartmentView.as_view(),
         name='department-display'),
    path('department/add/', DepartmentAdd.as_view(), name='department-add'),
    path('department/<int:id>/edit/', DepartmentEdit.as_view(), name='department-edit'),
    path('department/del/', DepartmentDelete.as_view(),
         name='department-delete'),

    # 用户管理
    path('user/<int:id>/', UserView.Edit.as_view(), name='user-edit'),
    path('user/display/', UserView.List.as_view(), name='user-display'),
    path('user/add/', UserView.Create.as_view(), name='user-add'),
    path('user/del/', UserView.Del.as_view(), name='user-del'),

    #职位管理
    path('post/display/', rbacview.PostView.as_view(),name='post-display'),
    path('post/add/', rbacview.PostAdd.as_view(),name='post-add'),
    path('post/del/', rbacview.PostDelete.as_view(),name='post-del'),
]
