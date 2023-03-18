from django import template

register = template.Library()

@register.simple_tag
def getvalue(dict, key):
    return dict.get(key)

def getnum(dict):
    return dict['usd_price']