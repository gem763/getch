from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from custom_user.models import AbstractEmailUser
from IPython.core.debugger import set_trace

from django.core.files.base import ContentFile
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from datetime import datetime
import requests
import urllib



class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True



# class ChannelBase(BigIdAbstract):
class Channel(BigIdAbstract):
    name = models.CharField(max_length=120, blank=False, null=False)
    keywords = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nlikes = models.IntegerField(default=0)
    master = models.ForeignKey('User', blank=True, null=True, on_delete=models.SET_NULL)
    # pix = models.ImageField(upload_to=_image_pix_path, blank=True, null=True)
    # pix_set = GenericRelation(Pix, blank=True)
    # avatar_set = GenericRelation(Avatar, blank=True)

    # class Meta:
    #     abstract = True

    def __str__(self):
        return self.name


class User(AbstractEmailUser, Channel):
    nickname = models.CharField(max_length=120, blank=False, null=False)

    def init_user(self):
        self.name = self.email
        self.nickname = self.email.split('@')[0]
        self.keywords = ', '.join([self.name, self.nickname])
        self.master = self
        self.save()

    def set_social_avatar(self):
        avatar_url = self.socialaccount_set.all()[0].get_avatar_url()
        resp = requests.get(avatar_url)

        if resp.status_code == 200:
            try:
                print(1,'*********************')
                avatar = Avatar.objects.get(on=self, avatar_type='social')

            except Avatar.DoesNotExist:
                print(2,'*********************')
                avatar = Avatar.objects.create(on=self, avatar_type='social')

            except Avatar.MultipleObjectsReturned:
                print(3,'*********************')
                print('social avatar duplicated')
                # social avatar가 여러개 있으면 우선 다 지워라(이럴리가 없긴하다)
                # 이 경우, 기존 social avatar의 selected는 무시된다
                Avatar.objects.filter(on=self, avatar_type='social').delete()
                avatar = Avatar.objects.create(on=self, avatar_type='social')

            fname = urllib.parse.quote_plus(avatar_url)
            avatar.src.save(fname, ContentFile(resp.content), save=True)
            print(avatar)
            print(avatar.on.__class__.__name__)
            print(avatar.on)
            return avatar

        else:
            return None


def _image_path(instance, fname):
    channel_type = instance.on.__class__.__name__.lower()
    name = instance.on.name
    image_type = instance.__class__.__name__.lower()
    fname = str(instance.created_at) + '__' + fname
    return '{channel_type}/{name}/{image_type}/{fname}'.format(channel_type=channel_type, name=name, image_type=image_type, fname=fname)


class Image(BigIdAbstract):
    # limit = models.Q(model='getchapp.user')
    # content_type = models.ForeignKey(ContentType, limit_choices_to=limit, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # on = GenericForeignKey('content_type', 'object_id')

    on = models.ForeignKey(Channel, blank=True, null=True, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    src = models.ImageField(upload_to=_image_path, blank=False, null=False, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        _selected = '[v]' if self.selected else '[ ]'
        return _selected + ' ' + self.on.name

    def select(self):
        image_type = self.__class__.__name__.lower()
        images = []

        if image_type=='pix':
            images = self.on.pix_set.all()
        elif image_type=='avatar':
            images = self.on.avatar_set.all()

        for image in images:
            if image.id==self.id:
                image.selected = True
            else:
                image.selected = False

            image.save()


class Pix(Image):
    pass
    # on = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='images')

class Avatar(Image):
    SOCIAL = 'social'
    UPLOADED = 'uploaded'
    AVATAR_TYPE_CHOICES = [(SOCIAL, 'social'), (UPLOADED, 'uploaded'),]
    avatar_type = models.CharField(max_length=10, choices=AVATAR_TYPE_CHOICES, default=UPLOADED)
