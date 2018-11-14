from django.urls import path
from . import views

app_name = 'workbench'

urlpatterns = [
    path('', views.index, name = "index"),
    path('user_config/', views.UserConfig.as_view(), name = "user_config"),
    path('message/', views.message, name = "message"),
    path('order/created/', views.Order.created, name = "Order.created"),
    path('order/received/', views.Order.received, name = "Order.received"),
    path('order/examine/', views.Order.examine, name = "Order.examine"),
    path('order/overview/', views.Order.overview, name = "Order.overview"),
    path('doc/', views.doc, name = "doc"),

]