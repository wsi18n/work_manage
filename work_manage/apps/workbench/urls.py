from django.urls import path
from . import views

app_name = 'workbench'

urlpatterns = [
    path('', views.index, name = "index"),
    path('upload/', views.upload, name="upload"),

    path('user_config/', views.UserConfig.as_view(), name = "UserConfig"),
    path('message/', views.MessageView.as_view(), name = "Message"),

    path('plan/list/<int:staff_plan>/', views.PlanView.List.as_view(), name = "Plan.List"),
    path('plan/overview/', views.PlanView.Overview.as_view(), name = "Plan.Overview"),
    path('plan/<int:id>/edit/', views.PlanView.Edit.as_view(), name = "Plan.Edit"),
    path('plan/new/<int:parent_id>/', views.PlanView.New.as_view(), name = "Plan.New"),
    path('plan/<int:id>/detail/', views.PlanView.Detail.as_view(), name="Plan.Detail"),
    path('plan/<int:id>/delete/', views.PlanView.Delete.as_view(), name="Plan.Delete"),

    path('doc/', views.Doc.as_view(), name = "Doc"),

]