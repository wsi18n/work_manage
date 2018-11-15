from django.urls import path
from . import views

app_name = 'workbench'

urlpatterns = [
    path('', views.index, name = "index"),
    path('user_config/', views.UserConfig.as_view(), name = "UserConfig"),
    path('message/', views.Message.as_view(), name = "Message"),
    path('plan/created/', views.Plan.Created.as_view(), name = "Plan.Created"),
    path('plan/received/', views.Plan.Received.as_view(), name = "Plan.Received"),
    path('plan/examine/', views.Plan.Examine.as_view(), name = "Plan.Examine"),
    path('plan/overview/', views.Plan.Overview.as_view(), name = "Plan.Overview"),
    path('plan/<int:id>/detail/', views.Plan.Detail.as_view(), name = "Plan.Detail"),

    path('doc/', views.Doc.as_view(), name = "Doc"),

]