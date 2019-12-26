from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from custom_user.models import AbstractEmailUser
from IPython.core.debugger import set_trace

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from datetime import datetime


class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


def channel_path(instance, fname, field):
    chtype = instance.__class__.__name__.lower()
    fname = str(datetime.now()) + '__' + fname
    return '{chtype}/{name}/{field}/{fname}'.format(chtype=chtype, name=instance.name, field=field, fname=fname)


def channel_image_path(instance, fname):
    return channel_path(instance, fname, 'image')

def channel_avatar_path(instance, fname):
    return channel_path(instance, fname, 'avatar')


class ChannelBase(BigIdAbstract):
    name = models.CharField(max_length=120, blank=False, null=False)
    keywords = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nlikes = models.IntegerField(default=0)
    master = models.ForeignKey('User', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=channel_image_path, blank=True, null=True)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     pk = self.pk
    #     super().save(*args, **kwargs)
    #
    #     if pk is None:
    #         Channel.objects.create(of=self)

    def __str__(self):
        return str(self.name)


# class Account(AbstractEmailUser, BigIdAbstract):
#     class Meta:
#         verbose_name = 'Account'
#         verbose_name_plural = 'Accounts'
#
#     def save(self, *args, **kwargs):
#         created = not self.pk
#         super().save(*args, **kwargs)
#
#         if created:
#             user = User()
#             user.account = self
#             user.name = self.email.split('@')[0]
#             user.keywords = user.name
#             user.save()
#             user.master = user
#             user.save()
#             print(self.socialaccount_set.all())
#             # User.objects.create(account=self, name=self.email.split('@')[0])


# class User(ChannelBase):
#     account = models.OneToOneField(Account, on_delete=models.CASCADE)
#
#     # def save(self, *args, **kwargs):
#     #     created = not self.pk
#     #     super().save(*args, **kwargs)
#     #
#     #     if created:
#     #         self.keywords = self.name
#     #         self.master = self
#     #
#     #         # socialaccounts = self.account.socialaccount_set.all()
#     #         # # print(self)
#     #         # # print(self.socialaccount_set)
#     #         # # print(self.socialaccount_set.all()[0].get_avatar_url())
#     #         # if len(socialaccounts) == 0:
#     #         #     self.image = 'user/default/icons8-user-100.png'
#     #         # else:
#     #         #     self.image = socialaccounts[0].get_avatar_url()
#     #
#     #         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return str(self.account.email)

class User(AbstractEmailUser, ChannelBase):
    nickname = models.CharField(max_length=120, blank=False, null=False)
    avatar = models.ImageField(upload_to=channel_avatar_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        if created:
            self.name = self.email
            self.nickname = self.email.split('@')[0]
            self.keywords = ', '.join([self.name, self.nickname])
            self.master = self
            super().save(*args, **kwargs)

    # def natural_key(self):
    #     return {'id':self.pk, 'image':self.user.socialaccount_set.all()[0].get_avatar_url(), 'email':self.user.email}
