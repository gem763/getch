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


class CustomEmailUser(AbstractEmailUser, BigIdAbstract):
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            # keywords = ', '.join([self.email, self.uid, self.extra_data.first_name, self.extra_data.last_name, self.extra_data.name])
            Profile.objects.create(name=self.email, keywords='', user=self)



class Channel(models.Model):
    limit = models.Q(app_label='getchapp', model='brand') | models.Q(app_label='getchapp', model='profile') | models.Q(app_label='getchapp', model='item')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    of = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '[{type}] {of}'.format(type=self.content_type, of=self.of)

    # def feeds(self):
    #     return self.feed_set.all().prefetch_related('hashtags').select_related('author').order_by('-timestamp')



class ChannelBase(models.Model):
    name = models.CharField(max_length=120, blank=False, null=False)
    keywords = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    nlikes = models.IntegerField(default=0)
    #type = models.CharField(max_length=50, blank=True, null=True)
    channel = GenericRelation(Channel, related_query_name='channel')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        pk = self.pk
        super().save(*args, **kwargs)

        if pk is None:
            #self.type = self.__class__.__name__.lower()
            Channel.objects.create(of=self)

    def __str__(self):
        return str(self.name)



class Profile(BigIdAbstract, ChannelBase):
    user = models.OneToOneField(CustomEmailUser, on_delete=models.CASCADE)


class Brand(ChannelBase):
    fullname_kr = models.CharField(max_length=120, blank=True, null=True)
    fullname_en = models.CharField(max_length=120, blank=True, null=True)
    origin = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='brand_images', default='') # 로고는 필수 (null=True 하면 안됨)
    master = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)

    # def __str__(self):
    #     return '{fullname_en}'.format(fullname_en=self.fullname_en)
        # return self.fullname_en.capitalize()


class Item(ChannelBase):
    image = models.ImageField(upload_to='item_images', default='')
    master = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)



def post_image_path(instance, fname):
    author = instance.author
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    fname = str(now) + '__' + fname
    return 'post_images/{author}/{year}/{month}/{day}/{fname}'.format(author=author, fname=fname, year=year, month=month, day=day)


class PostBase(BigIdAbstract):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=post_image_path)
    text = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nlikes = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return '{created_at} {email}'.format(created_at=self.created_at, email=self.author.user.email)



class Comment(PostBase):
    image = models.ImageField(upload_to=post_image_path, blank=True)
    limit = models.Q(app_label='getchapp', model='post') | models.Q(app_label='getchapp', model='tag')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    on = GenericForeignKey('content_type', 'object_id')


class Post(PostBase):
    def get_absolute_url(self):
        url = reverse_lazy('post', kwargs={'pk':self.pk})
        return url


class Tag(PostBase):
    image = models.ImageField(upload_to=post_image_path, blank=True)
    on = models.ForeignKey(Post, on_delete=models.CASCADE)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rates = models.IntegerField(default=0)



# Post도 channel 이다!~~~~~~~~~~~~~~~~~~~~
# class Post(BigIdAbstract):
#     author = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=post_image_path)
#     text = models.TextField(max_length=500, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return '{created_at} {email}'.format(created_at=self.created_at, email=self.author.user.email)
#
#     def get_absolute_url(self):
#         url = reverse_lazy('post', kwargs={'pk':self.pk})
#         return url
