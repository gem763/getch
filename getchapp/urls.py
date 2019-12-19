from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('accounts/', include('allauth.urls')),
    path('posting/', v.posting, name='posting'),
    path('my/', v.my, name='my'),

    path('post/<int:pk>/', v.post, name='post'),
    path('post/<int:pk>/save_tag/', v.save_tag, name='save_tag'),
    path('feed/tag/<int:pk>/', v.tag_feed, name='tag_feed'),

    path('comment/<int:pk>/', v.comment, name='comment'),
    path('tag/<int:pk>/', v.tag, name='tag'),

    path('channel/brand/<int:pk>/', v.brand, name='brand'),
    path('channel/item/<int:pk>/', v.item, name='item'),
    path('channel/profile/<int:pk>/', v.profile, name='profile'),
]
