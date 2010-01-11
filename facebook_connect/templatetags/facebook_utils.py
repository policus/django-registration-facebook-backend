from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('facebook_javascript.html')
def facebook_javascript():
    return { 'facebook_api_key': settings.FACEBOOK_API_KEY }

@register.inclusion_tag('facebook_register.html')
def facebook_register():
    return {}

@register.inclusion_tag('facebook_login.html')
def facebook_login():
    return {}