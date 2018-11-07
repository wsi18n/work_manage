from django.urls import path
from . import views

app_name = 'workbench'

urlpatterns = [
    path('', views.index, name = "index"),
    path('user_config/', views.user_config, name = "user_config"),
    path('message/', views.message, name = "message"),
    path('order/created/', views.Order.created, name = "Order.created"),
    path('order/received/', views.Order.received, name = "Order.received"),
    path('order/examine/', views.Order.examine, name = "Order.examine"),
    path('order/overview/', views.Order.overview, name = "Order.overview"),
    path('doc/', views.doc, name = "doc"),

]
'''
context.update(
        {'menu': {
            '个人中心': reverse('user_config'),
            '我的消息': reverse('message'),
            '工单管理':{
                '我创建的工单':reverse('Order.created'),
                '我收到的工单':reverse('Order.received'),
                '我审批的工单':reverse('Order.examine'),
                '工单总览':reverse('Order.overview'),
            },
            '我的文档': reverse('doc'),

        }}
    )
'''