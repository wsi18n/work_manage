from django.views.generic.base import View as _View
from django.contrib.auth.decorators import login_required

class View(_View):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(View, cls).as_view(*args, **kwargs)
        return login_required(view, login_url='/login/')