from django import template
from getchapp.models import User
# from django.template.loader import render_to_string

register = template.Library()


@register.filter
def like(user, ch):
    return user.likes.filter(pk=ch.pk).exists()

@register.filter
def bookmark(user, ch):
    return user.bookmarks.filter(pk=ch.pk).exists()


# @register.filter
# def file_exists(filepath):
#     if default_storage.exists(filepath):
#         print(default_storage)
#         return filepath
#
#     else:
#         return None


# @register.filter
# def of_name(namepair):
#     return Brand.objects.filter(name__in=namepair)
