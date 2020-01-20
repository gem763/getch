from django.db import models
from django.conf import settings
# from django.urls import reverse_lazy
from django.shortcuts import resolve_url

from django.db.models import Q
from django.core.files.base import ContentFile
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from model_utils.managers import InheritanceManager
from custom_user.models import AbstractEmailUser

from IPython.core.debugger import set_trace
from datetime import datetime
import requests
import urllib

# https://github.com/shanbay/django-vote
# from vote.models import VoteModel
# from vote.managers import VotableManager


GETCH_MASTER = 'get.ch@getch.com'



class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


def _default_master():
    return User.objects.get(email=GETCH_MASTER)


class Channel(BigIdAbstract):
    name = models.CharField(max_length=120, blank=False, null=False)
    keywords = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nlikes = models.IntegerField(default=0)
    nbookmarks = models.IntegerField(default=0)
    nreports = models.IntegerField(default=0)

    master = models.ForeignKey('User', blank=True, null=True, on_delete=models.SET(_default_master), related_name='mastering')
    on = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=500, blank=True, null=True)
    pix = models.ForeignKey('Pix', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
    avatar = models.ForeignKey('Avatar', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    objects = InheritanceManager() #https://dgkim5360.tistory.com/entry/django-model-inheritance

    def __str__(self):
        return self.name

    '''
    Channel의 child로 downcast
    '''
    def cast(self):
        for subclass in self.__class__.__subclasses__():
            try:
                return getattr(self, subclass.__name__.lower())
            except:
                pass

        return self

    # def on_channels(self):
    #     return self.channel_set.select_subclasses()

    def on_tags(self):
        return self.channel_set.exclude(tag__isnull=True)#.select_subclasses()

    def on_posts(self):
        return self.channel_set.exclude(post__isnull=True)#.select_subclasses()

    @property
    def typeof(self):
        return self.cast().__class__.__name__.lower()

    def get_absolute_url(self):
        # print('*******************', super().pk, self.pk)
        return resolve_url('channel', pk=self.pk)


class Brand(Channel):
    fullname_en = models.CharField(max_length=120, blank=True, null=True)
    fullname_kr = models.CharField(max_length=120, blank=True, null=True)
    origin = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=120, blank=True, null=True)

    def natural_key(self):
        return {'id':self.pk, 'avatar':self.avatar.src.url}


class Item(Channel):
    def natural_key(self):
        return {'id':self.pk, 'avatar':self.avatar.src.url}


class User(AbstractEmailUser, Channel):
    nickname = models.CharField(max_length=120, blank=False, null=False)
    likes = models.ManyToManyField(Channel, blank=True, related_name='users_liked')
    bookmarks = models.ManyToManyField(Channel, blank=True, related_name='users_bookmarked')

    def init_user(self):
        self.name = self.email
        self.nickname = self.email.split('@')[0]
        self.keywords = ', '.join([self.name, self.nickname])
        self.master = self
        self.save()

    def set_default_avatar(self):
        avatar_url = self.socialaccount_set.all()[0].get_avatar_url()
        resp = requests.get(avatar_url)

        if resp.status_code == 200:
            try:
                avatar = Avatar.objects.get(owner=self, default_on=self)

            except Avatar.DoesNotExist:
                avatar = Avatar.objects.create(owner=self, default_on=self)

            except Avatar.MultipleObjectsReturned:
                print('default avatar duplicated')
                # default avatar가 여러개 있으면 우선 다 지워라(이럴리가 없긴하다)
                # 이 경우, 기존 default avatar의 selected는 무시된다
                Avatar.objects.filter(owner=self, default_on=self).delete()
                avatar = Avatar.objects.create(owner=self, default_on=self)

            fname = urllib.parse.quote_plus(avatar_url)
            avatar.src.save(fname, ContentFile(resp.content), save=True)

            if self.avatar is None:
                self.avatar = avatar
                self.save()

    def natural_key(self):
        return {'id':self.pk, 'email':self.email, 'avatar':self.avatar.src.url}


class Post(Channel):
    pass


class Tag(Channel):
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    with_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    with_item = models.ForeignKey(Item, on_delete=models.CASCADE)

    # def natural_key(self):
    #     return {'id':self.pk, 'x':self.x, 'y':self.y, 'brand':self.with_brand.avatar.src, 'item':self.with_item.avatar.src}


def _image_path(instance, fname):
    owner = instance.owner.name
    type = instance.typeof
    default_on = instance.default_on
    fname = str(datetime.now()) + '__' + fname

    if default_on is None:
        fmt = '{owner}/{type}/{fname}'
        return fmt.format(owner=owner, type=type, fname=fname)

    else:
        chname = default_on.name
        fmt = '{owner}/{type}/{chname}/{fname}'
        return fmt.format(owner=owner, type=type, fname=fname, chname=chname)


class Image(BigIdAbstract):
    owner = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='%(class)s_owner_image_set')
    default_on = models.ForeignKey(Channel, blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_default_on_image_set')
    src = models.ImageField(upload_to=_image_path, blank=False, null=False, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.owner.name + ' | ' + str(self.created_at)

    @property
    def typeof(self):
        return self.__class__.__name__.lower()

    def natural_key(self):
        return self.src.url


class Pix(Image):
    pass

class Avatar(Image):
    pass
