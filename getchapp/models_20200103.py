from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from custom_user.models import AbstractEmailUser
from IPython.core.debugger import set_trace

from django.db.models import Q
from django.core.files.base import ContentFile
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from model_utils.managers import InheritanceManager

from datetime import datetime
import requests
import urllib


GETCH_MASTER = 'get.ch@getch.com'


class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


def default_master():
    return User.objects.get(email=GETCH_MASTER)


class Channel(BigIdAbstract):
    name = models.CharField(max_length=120, blank=False, null=False)
    keywords = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nlikes = models.IntegerField(default=0)
    master = models.ForeignKey('User', blank=True, null=True, on_delete=models.SET(default_master), related_name='mastering')
    on = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=500, blank=True, null=True)
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

    @property
    def typeof(self):
        return self.cast().__class__.__name__.lower()



class Brand(Channel):
    fullname_en = models.CharField(max_length=120, blank=True, null=True)
    fullname_kr = models.CharField(max_length=120, blank=True, null=True)
    origin = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=120, blank=True, null=True)


class Item(Channel):
    pass


class User(AbstractEmailUser, Channel):
    nickname = models.CharField(max_length=120, blank=False, null=False)

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
                avatar = Avatar.objects.get(on=self, owner=self, default=True)

            except Avatar.DoesNotExist:
                avatar = Avatar.objects.create(on=self, owner=self, default=True)

            except Avatar.MultipleObjectsReturned:
                print('default avatar duplicated')
                # default avatar가 여러개 있으면 우선 다 지워라(이럴리가 없긴하다)
                # 이 경우, 기존 default avatar의 selected는 무시된다
                Avatar.objects.filter(on=self, owner=self, default=True).delete()
                avatar = Avatar.objects.create(on=self, owner=self, default=True)

            fname = urllib.parse.quote_plus(avatar_url)
            avatar.src.save(fname, ContentFile(resp.content), save=True)
            return avatar

        else:
            return None



class Post(Channel):
    pass


class Tag(Channel):
    target = models.ForeignKey('Pix', on_delete=models.CASCADE)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    with_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    with_item = models.ForeignKey(Item, on_delete=models.CASCADE)


def _image_path(instance, fname):
    ch_type = instance.on.typeof
    ch_name = instance.on.name
    img_type = instance.typeof
    img_owner = instance.owner.name
    fname = str(instance.created_at) + '__' + fname
    fmt = '{ch_type}/{ch_name}/{img_type}/{img_owner}/{fname}'
    return fmt.format(ch_type=ch_type, ch_name=ch_name, img_type=img_type, img_owner=img_owner, fname=fname)


class Image(BigIdAbstract):
    on = models.ForeignKey(Channel, blank=False, null=False, on_delete=models.CASCADE)#, related_name='%(class)s_on')
    owner = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='+')#'%(class)s_owner')
    selected = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    src = models.ImageField(upload_to=_image_path, blank=False, null=False, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        _selected = '[v]' if self.selected else '[ ]'
        _by = ' | by ' + self.owner.name
        return _selected + ' ' + self.on.name + _by

    @property
    def typeof(self):
        return self.__class__.__name__.lower()

    def select(self):
        image_type = self.typeof
        images = []
        q = Q(owner__email=GETCH_MASTER) | Q(owner=self.owner)

        if image_type=='pix':
            images = self.on.pix_set.filter(q)
        elif image_type=='avatar':
            images = self.on.avatar_set.filter(q)

        for image in images:
            if image.id==self.id:
                image.selected = True
            else:
                image.selected = False

            image.save()


class Pix(Image):
    pass


class Avatar(Image):
    pass
