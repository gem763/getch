from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('accounts/', include('allauth.urls')),
    path('posting/', v.posting, name='posting'),
    path('my/', v.my, name='my'),
    path('my/<str:content>/', v.mycontents, name='mycontents'),
    # path('channel/brand/<int:pk>/', v.brand, name='brand'),
    # path('channel/item/<int:pk>/', v.item, name='item'),
    # path('channel/user/<int:pk>/', v.user, name='user'),


    path('channel/<int:pk>/', v.channel, name='channel'),
    path('channel/<int:pk>/delete/', v.channel_delete, name='channel_delete'),
    path('channel/<int:pk>/flag/', v.channel_flag, name='channel_flag'),
    path('channel/tag/save/', v.tag_save, name='tag_save'),
    path('channel/post/save/', v.post_save, name='post_save'),
    # path('channel/tag/<int:pk>/', v.tag, name='tag'),
    path('channel/<int:pk>/tagfeeds/', v.tagfeeds, name='tagfeeds'),
]
