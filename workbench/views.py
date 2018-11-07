from django.shortcuts import render,reverse


def _render(request, template, context= {}):
    context.update(
        {'menu': {
            '个人中心': reverse('workbench:user_config'),
            '我的消息': reverse('workbench:message'),
            '工单管理':{
                '我创建的工单':reverse('workbench:Order.created'),
                '我收到的工单':reverse('workbench:Order.received'),
                '我审批的工单':reverse('workbench:Order.examine'),
                '工单总览':reverse('workbench:Order.overview'),
            },
            '我的文档': reverse('workbench:doc'),

        }}
    )
    return render(request, template, context)


# Create your views here.
def index(request):
    return _render(request, 'workbench/index.html')

def user_config(request):
    return _render(request, 'workbench/user_config.html')

def message(request):
    return _render(request, 'workbench/index.html')

class Order:
    def created(request):
        return _render(request, 'workbench/index.html')
    def received(request):
        return _render(request, 'workbench/index.html')
    def examine(request):
        return _render(request, 'workbench/index.html')
    def overview(request):
        return _render(request, 'workbench/index.html')

def doc(request):
    return _render(request, 'workbench/index.html')
