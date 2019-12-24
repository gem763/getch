from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from custom_user.models import AbstractEmailUser

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from datetime import datetime


class BigIdAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


def channel_image_path(instance, fname):
    chtype = instance.__class__.__name__.lower()

    if chtype=='user':
        fname = str(datetime.now()) + '__' + fname
        return '{chtype}/{name}/{fname}'.format(chtype=chtype, name=instance.name, fname=fname)


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


class User(AbstractEmailUser, ChannelBase):
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        if created:
            self.name = self.email
            self.keywords = self.email.split('@')[0]
            self.master = self

            socialaccounts = self.socialaccount_set.all()
            print(self)
            print(self.socialaccount_set)
            print(self.socialaccount_set.all()[0].get_avatar_url())
            if len(socialaccounts) == 0:
                self.image = 'user/default/icons8-user-100.png'
            else:
                self.image = socialaccounts[0].get_avatar_url()

            super().save(*args, **kwargs)

    # def natural_key(self):
    #     return {'id':self.pk, 'image':self.user.socialaccount_set.all()[0].get_avatar_url(), 'email':self.user.email}
