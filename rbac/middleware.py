import re
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,redirect


class RbacMiddleware(MiddlewareMixin):
    """
    检查用户URL访问权限
    """
    def process_request(self, request):
            request_url = request.path_info
            permission_url = request.session.get('permission_url_list')
            for url in settings.SAFE_URL:
                if re.match(url, request_url):
                    return None
            if not permission_url:
                return redirect('login')
            else:
                if request_url in permission_url:
                    return None
                else:
                    return render(request, 'layout/page404.html')
