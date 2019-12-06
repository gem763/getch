from django.contrib import admin
from getchapp.models import Brand, Profile, Item, Post, Tag, Comment, CustomEmailUser, Channel
# Register your models here.


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(CustomEmailUser)
admin.site.register(Channel)
admin.site.register(Brand)
admin.site.register(Profile)
admin.site.register(Item)
