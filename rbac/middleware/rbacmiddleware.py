import re
from portal_web.portal_web import settings
from django.shortcuts import redirect, HttpResponse, render, reverse
from django.utils.deprecation import MiddlewareMixin

'''
# 为避免一些BUG，把该类复制到此处进行继承
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
'''

class RbacMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        current_url = request.path_info

        for url in settings.VALID_URL:
            if re.match(url, current_url):
                return None

        permission_list = request.session.get('permission_url_list')
        if not permission_list:
            return redirect('login')

        flag = False
        for db_url in permission_list:
            regax = "^{}$".format(db_url)
            if re.match(regax, current_url):
                flag = True
                break
        if not flag:
            return HttpResponse('无权访问')