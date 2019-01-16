from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib import messages

from . import models
from users.models import UserProfile, Department, Post
import json
from django.http import HttpResponse
import re
from work_manage.admin.tools import render,render403,render404
from work_manage.admin import base


# 组织架构
class DepartmentView(base.View):

    def get(self, request):
        department_obj = Department.objects.all()
        return render(request, 'rbac/Department-display.html', {
            'department_obj': department_obj,
        })


class DepartmentEdit(base.View):

    def get(self, request, id):
        department_list = Department.objects.all()
        department = get_object_or_404(Department, pk=id)
        return render(request, 'rbac/Department-add.html', {
            'department_list': department_list,
            'department':department
        })

    def post(self, request, id):
        params_dict = {
            'name': request.POST['name'],
            'parent_id': request.POST.get('parent', None)
        }
        Department.objects.filter(pk=id).update(**params_dict)
        messages.success(request, '保存成功')
        return redirect(reverse('rbac:department-display'))

class DepartmentAdd(base.View):

    def get(self, request):
        department_list = Department.objects.all()
        return render(request, 'rbac/Department-add.html', {
            'department_list': department_list,
        })

    def post(self, request):
        params_dict = {
            'name':request.POST['name'],
            'parent_id':request.POST.get('parent',None)
        }
        Department.objects.create(**params_dict)
        messages.success(request, '新建成功')
        return redirect(reverse('rbac:department-display'))



class DepartmentDelete(base.View):
    # 组织删除
    def post(self, request):
        department_id = request.POST['department_id']
        try:
            Department.objects.get(id=department_id).disable()
            messages.error(request, '删除成功')

        except Exception as e:
            messages.error(request, '删除失败')
        return redirect(reverse('rbac:department-display'))


@login_required(login_url='/login/')
def index(request):

        return render(request, 'rbac/system_index.html')


class MenuView(base.View):
    """
    菜单管理
    """

    def get(self, request):
        return render(request, 'rbac/menu-display.html', {
            'menu_list': models.Menu.objects.all(),
        })


class MenuAdd(base.View):

    def get(self, request):
        menu_obj = models.Menu.objects.all().values('id', 'name')
        menu_list = []
        for item in menu_obj:
            menu_list.append(item)

        return render(request, 'rbac/menu-add.html', {
            'menu_list': menu_list,
        })

    def post(self, request):
        # 保存权限菜单
        if request.POST['parent'] == 'null':
            menu_obj = models.Menu.objects.create(name=request.POST['name'])
            if request.POST['url']:
                menu_obj.url = request.POST['url']
            menu_obj.save()
        else:
            menu_obj = models.Menu(name=request.POST['name'],
                                   parent_id=request.POST['parent'])
            if request.POST["url"]:
                menu_obj.url = request.POST["url"]
            menu_obj.save()
        return redirect(reverse('rbac:menu-display'))


class MenuDelete(base.View):
    # 菜单删除
    def post(self, request):
        del_id = request.POST.get("del_id")
        ret = {
            "status": True,

        }
        try:
            del_obj = models.Menu.objects.get(id=del_id).disable()
            return HttpResponse(json.dumps(ret))
        except Exception as e:
            ret["status"] = False
            return HttpResponse(json.dumps(ret))


class RoleView:
    """
    角色管理
    """
    class List(base.View):
        def get(self, request):

            role = models.Role.objects.all()
            menu_obj = models.Menu.objects.all().order_by('id').values('name', 'id')

            return render(request, 'rbac/role-display.html', {
                'role': role,
                'menu_list': menu_obj,
            })

    class Edit(base.View):

        @classmethod
        def get(cls, request, id):
            role = get_object_or_404(models.Role, pk=id)
            all_menu = models.Menu.objects.all()
            all_users = UserProfile.objects.all()
            return render(request, 'rbac/role_edit.html', {
                'role': role,
                'all_menu':all_menu,
                'all_users':all_users
            })
        @classmethod
        def post(cls, request, id):
            role = get_object_or_404(models.Role, pk=id)
            if request.POST.get('related_menu[]'):
                permissions = request.POST.getlist('related_menu[]')  # [1,3,...]
                role.permission.clear()
                role.permission.add(*permissions)

            if request.POST.get('related_user[]'):
                related_users = request.POST.getlist('related_user[]') #[1,3,...]
                role.users_set.clear()
                role.users_set.add(*related_users)

            role.save()
            messages.success(request, '保存成功')

            return cls.get(request, id)

    class Add(base.View):

        def get(self, request):
            menu_obj = models.Menu.objects.all().values('name', 'id')
            menu_list = []
            for item in menu_obj:
                menu_list.append(item)
            return render(request, 'rbac/role-add.html', {
                'menu_list': menu_list,
            })

        def post(self, request):

            if not request.POST.getlist('check_val[]'):
                try:
                    if not request.POST.getlist('checked'):
                        role_obj = models.Role.objects.create(
                            name=request.POST['name'])
                        role_obj.save()
                    else:
                        role_obj = models.Role(name=request.POST['name'])
                        role_obj.save()
                        models.Role.objects.get(
                            name=request.POST['name']).permission.set(
                            request.POST.getlist('checked'))
                    return redirect(reverse('rbac:role-display'))
                except Exception as e:
                    return render403(request)
            else:
                mes = {'status': True, 'message': []}
                try:
                    check_val = request.POST.getlist('check_val[]')
                    role_name = request.POST.get('role_name')
                    role_id = request.POST.get('role_id')
                    role_obj = models.Role.objects.get(id=role_id)
                    role_obj.name = role_name
                    role_obj.permission.set(check_val)
                    role_obj.save()
                    return HttpResponse(json.dumps(mes))
                except Exception as e:
                    mes['message'].append('信息有误，请检查输入信息')
                    mes['status'] = False
                    return HttpResponse(json.dumps(mes))


    class Delete(base.View):
        # 角色删除
        def post(self, request):
            role_del_id = request.POST.get("role_del_id")
            ret = {
                "status": True
            }
            try:
                models.Role.objects.get(id=role_del_id).disable()
                return HttpResponse(json.dumps(ret))
            except Exception as e:
                ret["ststus"] = False
                return HttpResponse(json.dumps(ret))

class UserView:
    class Edit(base.View):
        @classmethod
        def get(cls, request, id):
            user = get_object_or_404(UserProfile, pk=id)
            return render(request, "users/user_edit.html", {
                "user_obj": user,
                "all_post": Post.objects.all(),
                "all_department": Department.objects.all()
            })

        @classmethod
        def post(cls, request, id):
            user = get_object_or_404(UserProfile, pk=id)
            if request.POST.get('gender'):
                user.gender = request.POST['gender']
            if request.POST.get('name'):
                user.alias = request.POST['name']
            if request.POST.get('birthday'):
                user.birthday = request.POST['birthday']
            if request.POST.get('joined_date'):
                user.joined_date = request.POST['joined_date']
            if request.POST.get('e-mail'):
                user.email = request.POST['e-mail']
            if request.POST.get('mobile'):
                user.mobile = request.POST['mobile']
            if request.POST.get('department'):
                user.department = get_object_or_404(Department, pk=request.POST['department'])
            if request.POST.get('post'):
                user.post = get_object_or_404(Post, pk=request.POST['post'])
            user.save()

            messages.success(request, '保存成功')

            return cls.get(request, id)
    class List(base.View):
        # 查看所有用户
        def get(self, request):
            user_obj = UserProfile.objects.all()
            return render(request, "users/user-display.html", {"user_obj": user_obj})

    class Create(base.View):
        # 新增用户
        @classmethod
        def get(cls, request):

            department_obj = Department.objects.all().values('id', 'name')
            post_obj = Post.objects.all()
            return render(request, 'users/user-add.html', {
                'department': department_obj,
                'post_obj': post_obj
            })
        @classmethod
        def post(cls, request):
            if request.POST['password'] == request.POST['re_password'] :
                if len(request.POST['password']) >= 5 :
                    if not UserProfile.objects.filter(username=request.POST['username']):

                        params_dict ={}
                        params_dict.update({'username':request.POST['username']})
                        params_dict.update({'password':request.POST['password']})
                        params_dict.update({'alias':request.POST.get('name',None)})
                        params_dict.update({'department_id':request.POST.get('department',None)})
                        params_dict.update({'post_id':request.POST.get('post_id',None)})

                        UserProfile.objects.create(**params_dict)
                        messages.success(request, '创建成功')

                        return redirect(reverse("rbac:user-display"))
                    else:
                        messages.error(request, '该用户名已存在')
                else:
                    messages.error(request, '密码过短')
            else:
                messages.error(request, '重复密码不一致')
            return cls.get(request)



    class Del(base.View):
        # 删除用户
        def post(self, request):
            ret = {"status": True, "msg": []}
            del_id = request.POST.get("user_delete_id")
            try:
                UserProfile.objects.get(id=del_id).disable()
            except Exception as e:
                ret["status"] = False
                ret["msg"] = '操作有误，请重新操作'
            return HttpResponse(json.dumps(ret))


class PostView(base.View):
    # 职位展示页面
    def get(self, request):
        post_obj = Post.objects.all()
        return render(request, 'users/post-display.html', {
            'post_obj': post_obj,
        })


class PostAdd(base.View):
    # 职位增加
    def get(self, request):
        return render(request, 'users/post-add.html')

    def post(self, request):
        msg = []
        message = {'status': True, 'msg': msg}

        if 'name' in request.POST:
            post_name = request.POST['name']
            post_is_leader = request.POST['is_leader']
            try:
                post_obj = Post.objects.create(
                    name=post_name,
                    is_leader=post_is_leader
                )
                post_obj.save()
            except Exception as e:
                msg = '输入信息有误'
                message['msg'].append(msg)

        elif 'post_edit_name' in request.POST:
            post_edit_id = request.POST['post_edit_id']
            post_edit_name = request.POST['post_edit_name']
            post_edit_is_leader = request.POST['post_edit_is_leader']

            try:
                post_edit_obj = Post.objects.get(id=post_edit_id)
                post_edit_obj.name = post_edit_name
                post_edit_obj.is_leader = post_edit_is_leader
                post_edit_obj.save()

            except Exception as e:
                msg = '输入信息有误'
                message['msg'].append(msg)
        return HttpResponse(json.dumps(message))


class PostDelete(base.View):
    # 职位删除
    def post(self, request):
        msg = []
        message = {'status': True, 'msg': msg}
        post_delete_id = request.POST['post_delete_id']
        try:
            post_obj = Post.objects.get(id=post_delete_id).disable()
        except Exception as e:
            msg = '操作失败'
            message['msg'].append(msg)
        return HttpResponse(json.dumps(message))
