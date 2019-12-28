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


def _path(instance, fname, field):
    chtype = instance.on.__class__.__name__.lower()
    name = instance.on.name
    # fname = str(datetime.now()) + '__' + fname
    fname = str(instance.created_at) + '__' + fname
    return '{chtype}/{name}/{field}/{fname}'.format(chtype=chtype, name=name, field=field, fname=fname)


def _image_path(instance, fname):
    return _path(instance, fname, 'image')

def _avatar_path(instance, fname):
    return _path(instance, fname, 'avatar')


class ChannelBase(BigIdAbstract):
    name = models.CharField(max_length=120, blank=False, null=False)
    keywords = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nlikes = models.IntegerField(default=0)
    master = models.ForeignKey('User', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=_image_path, blank=True, null=True)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     pk = self.pk
    #     super().save(*args, **kwargs)
    #
    #     if pk is None:
    #         Channel.objects.create(of=self)

    def __str__(self):
        return self.name


class User(AbstractEmailUser, ChannelBase):
    nickname = models.CharField(max_length=120, blank=False, null=False)

    def set_social_avatar(self):
        avatar_url = self.socialaccount_set.all()[0].get_avatar_url()
        resp = requests.get(avatar_url)

        if resp.status_code == 200:
            try:
                avatar = UserAvatar.objects.get(on=self, social=True)

            except UserAvatar.DoesNotExist:
                avatar = UserAvatar.objects.create(on=self, social=True)

            except UserAvatar.MultipleObjectsReturned:
                print('social avatar duplicated')
                # social avatar가 여러개 있으면 우선 다 지워라(이럴리가 없긴하다)
                # 이 경우, 기존 social avatar의 selected는 무시된다
                UserAvatar.objects.filter(on=self, social=True).delete()
                avatar = UserAvatar.objects.create(on=self, social=True)

            fname = urllib.parse.quote_plus(avatar_url)
            avatar.src.save(fname, ContentFile(resp.content), save=True)
            return avatar

        else:
            return None


class Avatar(BigIdAbstract):
    selected = models.BooleanField(default=False)
    src = models.ImageField(upload_to=_avatar_path, blank=False, null=False, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        _selected = '[v]' if self.selected else '[ ]'
        return _selected + ' ' + self.on.name

    def select(self):
        for avatar in self.on.avatar.all():
            if avatar.id==self.id:
                avatar.selected = True
            else:
                avatar.selected = False

            avatar.save()


class UserAvatar(Avatar):
    social = models.BooleanField(default=False)
    on = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='avatar')
