from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.urls import reverse
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from getchapp.models import Channel, User, Brand, Item, Post, Tag, Pix, Avatar
from .forms import TagForm, PostForm
from datetime import datetime

brands_search = list(Brand.objects.all().values('pk', 'name', 'avatar__src', 'category', 'fullname_kr', 'fullname_en', 'keywords').order_by('name'))
items_search = Item.objects.order_by('name')


def play(request):
    channels = Channel.objects.exclude(pix__isnull=True).order_by('-created_at')
    likes = request.user.likes.all()
    return render(request, 'getchapp/play.html', {'channels':channels, 'likes':likes})


def channelset(request):
    howmany = request.GET.get('howmany', 10)
    channels = Channel.objects.exclude(pix__isnull=True).order_by('-created_at')[:int(howmany)]
    return render(request, 'getchapp/channelset.html', {'channels':channels})


def intro(request):
    channels = Channel.objects.exclude(pix__isnull=True).order_by('-created_at')
    return render(request, 'getchapp/intro.html', {'channels':channels})
#
# # @login_required
def posting(request):
    pass
# def posting(request):
#     if request.method=='POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.author = get_object_or_404(Profile, user=request.user)
#             obj.save()
#             return redirect(obj)
#
#     else:
#         form = PostForm()
#         return render(request, 'getchapp/posting.html', {'form':form})
#
@login_required
def my(request):
    likes = request.user.likes.all()
    # bookmarks = request.user.bookmarks.all()
    return render(request, 'getchapp/my.html', {'likes':likes})


def mycontents(request, content):
    if content=='likes':
        channels = request.user.likes.all()

    elif content=='bookmarks':
        channels = request.user.bookmarks.all()

    return render(request, 'getchapp/mycontents.html', {'channels':channels})


def _create_pix(request):
    return Pix.objects.create(src=request.FILES['image'], owner=request.user)

def _create_tag(request):
    tag = Tag()
    tag.name = request.user.name + '__' + str(datetime.now())
    tag.keywords = ''
    tag.master = request.user
    tag.on_id = request.POST['on_id']
    tag.text = request.POST['text']
    tag.x = request.POST['x']
    tag.y = request.POST['y']
    tag.with_brand_id = request.POST['brand_id']
    tag.with_item_id = request.POST['item_id']

    if 'image' in request.FILES:
        tag.pix = _create_pix(request)

    tag.save()
    return tag

def _create_post(request):
    post = Post()
    post.name = request.user.name + '__' + str(datetime.now())
    post.keywords = ''
    post.master = request.user
    post.text = request.POST['text']

    if request.POST['on_id'] != 'none':
        post.on_id = request.POST['on_id']

    if 'image' in request.FILES:
        post.pix = _create_pix(request)

    post.save()
    return post


def tag_save(request):
    if request.method=='POST':
        tag = _create_tag(request)
        return render(request, 'getchapp/tags.html', {'ch':tag.on, 'saved':tag.pk})


def post_save(request):
    if request.method=='POST':
        post = _create_post(request)

        if request.POST['on_id'] != 'none':
            return render(request, 'getchapp/posts.html', {'ch':post.on})
        else:
            return JsonResponse({'ch_id':post.pk}, safe=False)


def tagfeeds(request, pk):
    ch = Channel.objects.get(pk=pk)
    return render(request, 'getchapp/tagfeeds.html', {'ch':ch})


def channel(request, pk):
    ch = Channel.objects.get(pk=pk)
    ctx = {'ch':ch, 'chtype':ch.typeof, 'brands':brands_search, 'items':items_search}
    return render(request, 'getchapp/channel.html', ctx)


def channel_delete(requst, pk):
    ch = Channel.objects.get(pk=pk)
    ch.delete()
    return HttpResponseRedirect(reverse('intro'))


@login_required
def channel_flag(request, pk):
    action = request.GET.get('action', None)
    tobe = request.GET.get('tobe', None)
    chs = Channel.objects.filter(pk=pk)

    if action=='like':
        myflags = request.user.likes
        nfield = 'nlikes'

    elif action=='bookmark':
        myflags = request.user.bookmarks
        nfield = 'nbookmarks'

    if tobe=='on':
        myflags.add(chs[0])
        chs.update(**{nfield:F(nfield)+1})

    else:
        myflags.remove(chs[0])
        chs.update(**{nfield:F(nfield)-1})

    return JsonResponse({'action':action, 'tobe':tobe}, safe=False)



# def save_tag(request, pk):
#     resp_fail = JsonResponse({'success':False})
#
#     if request.method=='POST':
#         try:
#             tagform = TagForm(request.POST, request.FILES)
#             if tagform.is_valid():
#                 obj = tagform.save(commit=False)
#                 obj.on_id = pk
#                 obj.x = request.POST['x']
#                 obj.y = request.POST['y']
#                 obj.brand_id = request.POST['brand_id']
#                 obj.item_id = request.POST['item_id']
#                 obj.author = get_object_or_404(Profile, user=request.user)
#                 obj.save()
#
#                 # _tags = serializers.serialize('python', Tag.objects.filter(on__pk=pk), use_natural_foreign_keys=True)
#                 # return JsonResponse({'success':True, 'tags':_tags}, safe=False)
#                 _tags = Tag.objects.filter(on__pk=pk).values('pk', 'x', 'y', 'brand__image', 'item__image')
#                 return JsonResponse({'success':True, 'tags':list(_tags)}, safe=False)
#
#             else:
#                 return resp_fail
#
#         except:
#             return resp_fail
#
#     else:
#         return resp_fail
