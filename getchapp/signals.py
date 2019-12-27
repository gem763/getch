from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from getchapp.models import User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        instance.name = instance.email
        instance.nickname = instance.email.split('@')[0]
        instance.keywords = ', '.join([instance.name, instance.nickname])
        instance.master = instance
        instance.save()


@receiver(m2m_changed, sender=User.socialaccount_set.through)
def socialaccount_post_add(sender, instance, action='post_add', **kwargs):
    print('*******************')
