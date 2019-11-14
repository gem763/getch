from django.db import models
from django.conf import settings
from custom_user.models import AbstractEmailUser

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class CustomEmailUser(AbstractEmailUser, BigIdAbstract):
    pass



# class Profile(BigIdAbstract):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.email



# class Channel(models.Model):
#     limit = models.Q(app_label='app', model='brand') | models.Q(app_label='app', model='customchannel')
#     content_type = models.ForeignKey(ContentType, limit_choices_to=limit, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content = GenericForeignKey('content_type', 'object_id')
#     master = models.ForeignKey('Profile', blank=True, null=True, on_delete=models.SET_NULL)
#     created_at = models.DateTimeField(auto_now_add=True)
#     nlikes = models.IntegerField(default='0')
#
#     def __str__(self):
#         return str(self.content)
#         # return str(self.created_at)
#
#     def feeds(self):
#         return self.feed_set.all().prefetch_related('hashtags').select_related('author').order_by('-timestamp')
#
#
# class Customchannel(models.Model):
#     name = models.CharField(max_length=120)
#     keywords = models.TextField(max_length=500, blank=True, null=True)
#     description = models.TextField(max_length=500, blank=True, null=True)
#     image = models.ImageField(upload_to='customchannel_images', default='') # 로고는 필수 (null=True 하면 안됨)
#
#     channels = GenericRelation(Channel, related_query_name='channel')
#
#     def __str__(self):
#         return self.name
#
#
class Brand(models.Model):
    name = models.CharField(max_length=120)
    fullname_kr = models.CharField(max_length=120, blank=True, null=True)
    fullname_en = models.CharField(max_length=120, blank=True, null=True)
    keywords = models.TextField(max_length=500, blank=True, null=True)
    # website = models.CharField(max_length=200, blank=True, null=True)
    origin = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='brand_images', default='') # 로고는 필수 (null=True 하면 안됨)

    def __str__(self):
        return self.fullname_en.capitalize()



class Post(BigIdAbstract):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/origin')
    content = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{created_at} {email}'.format(created_at=self.created_at, email=self.author.email)
