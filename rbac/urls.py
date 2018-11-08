from django.urls import path
from .views import *
app_name = 'rbac'


urlpatterns = [
    #权限菜单
    path('menu/',MenuView.as_view(), name="menu-list"),
    path('menu/add/',MenuAdd.as_view(),name='menu-add'),


    #角色菜单
    path('role/',RoleView.as_view(),name='role-list'),
    path('role/add/',RoleAdd.as_view(),name='role-add'),

]