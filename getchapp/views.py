from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.contrib.auth.decorators import login_required
from getchapp.models import Channel, User, Brand, Item, Post, Tag, Pix, Avatar
from .forms import TagForm, PostForm
from datetime import datetime


brands_all = Brand.objects.all()
items_all = Item.objects.all()
brands_search = list(brands_all.values('pk', 'name', 'avatar__src', 'category', 'fullname_kr', 'fullname_en', 'keywords').order_by('name'))
items_search = list(items_all.values('pk', 'name', 'avatar__src', 'keywords').order_by('name'))


def intro(request):
    # posts = Post.objects.order_by('-created_at')
    channels = Channel.objects.order_by('-created_at')
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
#
def my(request):
    return render(request, 'getchapp/my.html')


def _create_pix(request):
    return Pix.objects.create(src=request.FILES['image'], owner=request.user)

def _create_tag(request):
    tag = Tag()
    tag.name = request.user.name + '__' + str(datetime.now())
    tag.keywords = ''
    tag.master = request.user
    tag.on_id = request.POST['ch_id']
    tag.text = request.POST['text']
    tag.x = request.POST['x']
    tag.y = request.POST['y']
    tag.with_brand_id = request.POST['brand_id']
    tag.with_item_id = request.POST['item_id']

    if 'image' in request.FILES:
        tag.pix = _create_pix(request)

    tag.save()
    return tag


# def tag_save(request):
#     if request.method=='POST':
#         try:
#             tag = _create_tag(request)
#             # tags = Tag.objects.filter(on__pk=tag.on_id).values('pk', 'x', 'y', 'with_brand__avatar__src', 'with_item__avatar__src')
#             tags = serializers.serialize('python', Tag.objects.filter(on__pk=tag.on_id), use_natural_foreign_keys=True)
#             return JsonResponse({'success':True, 'tags':tags}, safe=False)
#
#         except:
#             return JsonResponse({'success':False}, safe=False)


def tag_save(request):
    if request.method=='POST':
        tag = _create_tag(request)
        return render(request, 'getchapp/post-tags.html', {'post':tag.on})


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


# def tagfeeds(request, pk):
#     if request.method=='GET':
#         # tags = Tag.objects.filter(pk=pk)
#         # tags = Channel.objects.filter(tag__isnull=False, tag__pk=pk)
#         # tag = serializers.serialize('python', tags, use_natural_foreign_keys=True)[0]
#         # feeds = serializers.serialize('python', tags[0].on_posts(), use_natural_foreign_keys=True)
#
#         tags = Tag.objects.filter(pk=pk)
#         tag = tags.values('pk', 'master', 'master__avatar__src', 'master__email', 'text', 'created_at', 'pix__src', 'with_brand__avatar__src', 'with_item__avatar__src')[0]
#         feeds = serializers.serialize('python', tags[0].channel_set.all(), use_natural_foreign_keys=True)
#         return JsonResponse({'success':True, 'tag':tag, 'feeds':feeds}, safe=False)


# def tagfeeds(request, pk):
#     if request.method=='GET':
#         tag = Tag.objects.get(pk=pk)
#         return render(request, 'getchapp/post-feeds.html', {'post':tag})
#
#
# def tag(request, pk):
#     _post = Tag.objects.get(pk=pk)
#     ctx = {'post':_post, 'brands':brands_search, 'items':items_search}
#     return render(request, 'getchapp/post.html', ctx)


def feeds(request, pk):
    ch = Channel.objects.get(pk=pk)
    return render(request, 'getchapp/feeds.html', {'ch':ch})


def channel(request, pk):
    ch = Channel.objects.get(pk=pk)
    ctx = {'ch':ch, 'brands':brands_search, 'items':items_search}
    return render(request, 'getchapp/channel.html', ctx)


# def post(request, pk):
#     _post = get_object_or_404(Post, pk=pk)
#     ctx = {'post':_post, 'brands':brands_search, 'items':items_search}
#     return render(request, 'getchapp/post.html', ctx)


def user(request, pk):
    _user = get_object_or_404(User, pk=pk)
    return render(request, 'getchapp/user.html', {'user':_user})
