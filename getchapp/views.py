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

# brands_search = list(brands_all.values('pk', 'name', 'image', 'category', 'fullname_kr', 'fullname_en', 'keywords').order_by('name'))
# items_search = list(items_all.values('pk', 'name', 'image', 'keywords').order_by('name'))


def intro(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'getchapp/intro.html', {'posts':posts})
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
    tag.on_id = request.POST['post_id']
    tag.text = request.POST['text']
    tag.x = request.POST['x']
    tag.y = request.POST['y']
    tag.with_brand_id = request.POST['brand_id']
    tag.with_item_id = request.POST['item_id']

    if 'image' in request.FILES:
        tag.pix = _create_pix(request)

    tag.save()
    return tag


def tag_save(request):
    if request.method=='POST':
        try:
            tag = _create_tag(request)
            # tags = Tag.objects.filter(on__pk=tag.on_id).values('pk', 'x', 'y', 'with_brand__avatar__src', 'with_item__avatar__src')
            tags = serializers.serialize('python', Tag.objects.filter(on__pk=tag.on_id), use_natural_foreign_keys=True)
            return JsonResponse({'success':True, 'tags':tags}, safe=False)

        except:
            return JsonResponse({'success':False}, safe=False)



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


def tagfeeds(request, pk):
    if request.method=='GET':
        # tags = Tag.objects.filter(pk=pk)
        # tags = Channel.objects.filter(tag__isnull=False, tag__pk=pk)
        # tag = serializers.serialize('python', tags, use_natural_foreign_keys=True)[0]
        # feeds = serializers.serialize('python', tags[0].on_posts(), use_natural_foreign_keys=True)

        tags = Tag.objects.filter(pk=pk)
        tag = tags.values('pk', 'master', 'master__avatar__src', 'master__email', 'text', 'created_at', 'pix__src', 'with_brand__avatar__src', 'with_item__avatar__src')[0]
        feeds = serializers.serialize('python', tags[0].channel_set.all(), use_natural_foreign_keys=True)
        return JsonResponse({'success':True, 'tag':tag, 'feeds':feeds}, safe=False)


# def tag_feed(request, pk):
#     resp_fail = JsonResponse({'success':False})
#
#     if request.method=='GET':
#         tag = serializers.serialize('python', Tag.objects.filter(pk=pk), use_natural_foreign_keys=True)[0]
#         comments = serializers.serialize('python', Comment.objects.filter(object_id=pk, content_type__model='tag'), use_natural_foreign_keys=True)
#         return JsonResponse({'success':True, 'tag':tag, 'comments':comments}, safe=False)
#
#
#
# def comment(request, pk):
#     _comment = get_object_or_404(Comment, pk=pk)
#     _tagform = TagForm()
#     ctx = {'post':_comment, 'brands':brands_search, 'items':items_search, 'tagform':_tagform}
#     return render(request, 'getchapp/post.html', ctx)
#
#
# def tag(request, pk):
#     _tag = get_object_or_404(Tag, pk=pk)
#     _tagform = TagForm()
#     ctx = {'post':_tag, 'brands':brands_search, 'items':items_search, 'tagform':_tagform}
#     return render(request, 'getchapp/post.html', ctx)


def tag(request, pk):
    _post = Tag.objects.get(pk=pk)
    ctx = {'post':_post, 'brands':brands_search, 'items':items_search}
    return render(request, 'getchapp/post.html', ctx)


def post(request, pk):
    _post = get_object_or_404(Post, pk=pk)
    # _tagform = TagForm()
    ctx = {'post':_post, 'brands':brands_search, 'items':items_search}#, 'tagform':_tagform}

    # if request.method=='POST':
    #     print('*******************************')
    #     pass
        # tagform = TagForm(request.POST, request.FILES)
        # print(request.FILES)
        # if tagform.is_valid():
        #     obj = tagform.save(commit=False)
        #     obj.on = _post
        #     obj.x = request.POST['x']
        #     obj.y = request.POST['y']
        #     obj.author = get_object_or_404(Profile, user=request.user)
        #     obj.brand = get_object_or_404(Brand, pk=request.POST['brand_id'])
        #     obj.item = get_object_or_404(Item, pk=request.POST['item_id'])
        #     obj.save()
        #     return redirect(_post)

    # else:
    return render(request, 'getchapp/post.html', ctx)



# def brand(request, pk):
#     _brand = get_object_or_404(Brand, pk=pk)
#     return render(request, 'getchapp/brand.html', {'brand':_brand})
#
#
# def item(request, pk):
#     _item = get_object_or_404(Item, pk=pk)
#     return render(request, 'getchapp/item.html', {'item':_item})
#
#
def user(request, pk):
    _user = get_object_or_404(User, pk=pk)
    return render(request, 'getchapp/user.html', {'user':_user})
