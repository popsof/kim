from django import template
from django.utils.dateparse import parse_datetime

register = template.Library()


@register.filter(name='str2date')
def str2date(value):
    return parse_datetime(value)