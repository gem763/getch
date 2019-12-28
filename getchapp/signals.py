from allauth.socialaccount.signals import social_account_updated#, pre_social_login
from allauth.account.signals import user_signed_up#, user_logged_in
from django.db.models.signals import post_save#, pre_save, m2m_changed
from django.dispatch import receiver
from getchapp.models import User, UserAvatar



@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        instance.name = instance.email
        instance.nickname = instance.email.split('@')[0]
        instance.keywords = ', '.join([instance.name, instance.nickname])
        instance.master = instance
        instance.save()


@receiver(social_account_updated)
def allauth_social_account_updated(request, sociallogin, **kwargs):
    # https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/models.py
    sociallogin.user.set_social_avatar()


@receiver(user_signed_up)
def allauth_user_signed_up(request, user, **kwargs):
    avatar = user.set_social_avatar()
    if avatar is not None:
        avatar.select()
        print(avatar.selected)
