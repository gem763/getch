from django.urls import path
from django.conf.urls import include
from . import views as v

urlpatterns = [
    path('', v.intro, name='intro'),
    path('accounts/', include('allauth.urls')),
    path('posting/', v.posting, name='posting'),
    path('my/', v.my, name='my'),

    path('post/<int:pk>/', v.post, name='post'),
    path('channel/brand/<int:pk>/', v.brand, name='brand'),
    path('channel/item/<int:pk>/', v.item, name='item'),
    path('channel/profile/<int:pk>/', v.profile, name='profile'),
]
