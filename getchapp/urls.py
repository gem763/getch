from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('accounts/', include('allauth.urls')),
    path('posting/', v.posting, name='posting'),
    path('my/', v.my, name='my'),
    # path('channel/brand/<int:pk>/', v.brand, name='brand'),
    # path('channel/item/<int:pk>/', v.item, name='item'),
    # path('channel/user/<int:pk>/', v.user, name='user'),


    path('channel/<int:pk>/', v.channel, name='channel'),
    path('channel/tag/save/', v.tag_save, name='tag_save'),
    # path('channel/tag/<int:pk>/', v.tag, name='tag'),
    path('channel/<int:pk>/feeds/', v.feeds, name='feeds'),
]
