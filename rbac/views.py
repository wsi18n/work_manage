from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models
from users.models import UserProfile
from django.http import HttpResponse
from django.views.generic.base import View
import json


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **init_kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**init_kwargs)
        return login_required(view)



@login_required(login_url='/login/')
def index(request):
    if request.user:
        bool_status = False   #权限管理页面是否展示
        user_name = request.user.username
        # 获取user对应的角色列表
        role_obj = UserProfile.objects.get(name=user_name).roles.all()
        #role_list = []
        permission_list = []#权限url列表

        for item in role_obj:
            #role_list.append(item)
            #permission_list.append(models.Menu.objects.filter(role__name=item).values('url').distinct())
            for item in models.Menu.objects.filter(role__name=item).values('url').distinct():
                permission_url_list = str(item['url'])
                permission_list.append(permission_url_list)
        request.session['permission_url_list'] = permission_list

        top_menu = models.Menu.objects.filter(parent__isnull=True).values('name','url')
        role_list = []
        for item in role_obj:
            role_list.append(str(item))
        if '管理员' in role_list:
            bool_status = True
    return render(request, 'rbac/system_index.html',{
        'top_menu':top_menu,
        'status':bool_status,
    })


class MenuView(LoginRequiredMixin, View):
    """
    菜单管理
    """
    def get(self, request):
        #url_now=request.path_info
        role_obj = UserProfile.objects.get(name = request.user.username).roles.all()
        menu = models.Menu.objects.all()
        role_list = []
        for item in role_obj:
            role_list.append(str(item))
        if request.user.is_authenticated and  '管理员' in role_list:
            top_menu = models.Menu.objects.filter(parent__isnull=True).values('name', 'url')
            return render(request, 'rbac/menu-list.html', {
                'menu_list':menu,
                'top_menu': top_menu,
            })
        else:
            return render(request,'layout/page404.html')

    def post(self, request):
        #菜单删除
        menu_obj = models.Menu.objects.get(id=request.POST['menu_delete']).delete()
        return HttpResponse('ok')


class MenuAdd(LoginRequiredMixin, View):

    def get(self, request):
        menu_obj = models.Menu.objects.all().values('id','name')
        menu_list = []
        for item in menu_obj:
            menu_list.append(item)

        return render(request, 'rbac/menu_detail.html',{
            'menu_list':menu_list,
        })

    def post(self, request):
        #保存权限菜单
        if request.POST['parent'] == 'null':
            menu_obj = models.Menu.objects.create(name=request.POST['name'],url=request.POST['url'])
            menu_obj.save()
        else:
            menu_obj = models.Menu(name=request.POST['name'],url=request.POST['url'],parent_id=request.POST['parent'])
            menu_obj.save()
        return HttpResponse('ok')






class RoleView(LoginRequiredMixin, View):
    """
    角色管理
    """
    def get(self, request):
        role_obj = UserProfile.objects.get(name=request.user.username).roles.all()
        role = models.Role.objects.all()
        role_list = []
        for item in role_obj:
            role_list.append(str(item))
        if request.user.is_authenticated and '管理员' in role_list:
            top_menu = models.Menu.objects.filter(parent__isnull=True).values('name', 'url')
            return render(request, 'rbac/role-list.html', {
                'role': role,
                'top_menu': top_menu,
            })
        else:
            return render(request, 'layout/page404.html')

    def post(self,request):
        #角色删除
        role_obj = models.Role.objects.get(id=request.POST['role_delete']).delete()
        return HttpResponse('ok')


class RoleAdd(LoginRequiredMixin, View):

    def get(self, request):
        menu_obj = models.Menu.objects.all().values('name','id')
        menu_list = []
        for item in menu_obj:
            menu_list.append(item)
        return render(request,'rbac/role_detail.html',{
            'menu_list':menu_list,
        })

    def post(self,request):
        if  not request.POST.getlist('checked'):
            role_obj = models.Role.objects.create(name=request.POST['name'])
            role_obj.save()
        else:
            role_obj = models.Role(name=request.POST['name'])
            role_obj.save()
            role_obj2 = models.Role.objects.get(name=request.POST['name']).permission.set(request.POST.getlist('checked'))
        return HttpResponse('ok')
