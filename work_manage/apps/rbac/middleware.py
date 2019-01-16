import re
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
from work_manage.admin.tools import render403
from users.models import UserProfile
from rbac.models import Menu



class RbacMiddleware(MiddlewareMixin):
    """
    检查用户URL访问权限
    """

    def process_request(self, request):
        request_url = request.path_info

        permission_url = request.session.get('permission_list')
        for url in settings.SAFE_URL:
            if re.match(url, request_url):
                return None
        if not permission_url:
            if request.user.is_authenticated:
                # 初始化权限
                roles = request.user.roles.all()
                permission_url = list(Menu.objects.filter(role__in=roles,url__isnull=False).values('url'))
                for i in range(len(permission_url)):
                    permission_url[i] = permission_url[i]['url']

                request.session['permission_list'] = permission_url
            else:
                return redirect(reverse('login'))

        if permission_url:
            for url in permission_url:
                if request_url == url:
                    return None
                elif re.match("^"+url+"$",request_url):
                    return None

        return render403(request)