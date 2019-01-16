from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db import models
import logging
logger = logging.getLogger(__name__)
register = template.Library()


def get_pk_list_from_queryset(queryset_obj):
    l = []
    for item in queryset_obj:
        l.append(item.pk)
    return l
'''
generate <options> in <select> by tuple_list 
tuple_list should be tuple list or django QuerySet object 
selected_options_value = should be int or int list or QuerySet object 

e.g.:
    params:
        tuple_list = [
            ('1','选项a'),
            ('2','选项b'),
            ('4','选项c'),
        ]
        selected_options_value = [1,4]
        
    return:
        "
        <options value="1" selected >选项a</options>
        <options value="2" >选项b</options>
        <options value="4" selected >选项c</options>
        "
'''
@register.simple_tag
def generate_options(tuple_list, selected_options_value=[]):
    if isinstance(selected_options_value,models.QuerySet):
        selected_options_value = get_pk_list_from_queryset(selected_options_value)
    elif not isinstance(selected_options_value,list):
        selected_options_value= [selected_options_value]

    content = ""
    for tup in tuple_list:
        if isinstance(tup, models.Model):
            tup = (tup.id, tup.__str__())
        if tup[0] in selected_options_value:
            content += '<option value="%s" selected>%s</option>' %( tup[0], tup[1])
        elif str(tup[0]) in selected_options_value:
            content += '<option value="%s" selected>%s</option>' %( tup[0], tup[1])
        else:
            content += '<option value="%s" >%s</option>' %( tup[0], tup[1])

    return mark_safe(content)

@register.filter(is_safe=True)
def choices_trans(value,tuple_name):
    from workbench.models import Plan
    PLAN_STATE = Plan.STATE

    for row in eval(tuple_name):
        if value == row[0]:
            return row[1]