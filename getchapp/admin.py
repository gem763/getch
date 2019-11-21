from django.contrib import admin
from getchapp.models import Brand, Profile, Item, Post, CustomEmailUser, Channel#, Customchannel
# Register your models here.


admin.site.register(Post)
admin.site.register(CustomEmailUser)
admin.site.register(Channel)
admin.site.register(Brand)
admin.site.register(Profile)
admin.site.register(Item)
