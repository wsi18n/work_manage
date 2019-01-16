import re
from django.shortcuts import render as jg_render
from django.contrib.auth.decorators import login_required

def render(request, template, context={},*args, **kwargs):
    user = request.user
    user_roles = user.roles.all()
    from rbac.models import Menu #函数内import 避免循环import报错
    # filter(role__in=user_roles, ...)会过滤没有权限的菜单，下同
    top_menu = Menu.objects.filter(role__in=user_roles, parent__isnull=True)

    # parent_menu为 根url的menu对象
    # 比如 url="/system/"的menu对象
    request_url = request.path_info
    parent_menu = None
    for menu in top_menu:
        if re.match(menu.url, request_url):
            parent_menu = menu
            break

    after_menu = Menu.objects.filter(role__in=user_roles, parent=parent_menu)
    for menu in after_menu:
        menu.children = Menu.objects.filter(role__in=user_roles, parent=menu)

    context.update({
        'top_menu': top_menu,
        'after_menu': after_menu,
    })
    return jg_render(request, template, context,*args, **kwargs)
def render404(request, *args, **kwargs):
    return render(request, 'page404.html', status=404, *args, **kwargs)

def render403(request, *args, **kwargs):
    return render(request, 'page403.html', status=403, *args, **kwargs)

class MyLoginRequest(object):
    @classmethod
    def as_view(cls, **init_kwargs):
        view = super(MyLoginRequest, cls).as_view(**init_kwargs)
        return login_required(view)
