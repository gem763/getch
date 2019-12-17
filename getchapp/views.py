from django.shortcuts import render, get_object_or_404, redirect
# from django.views.decorators.csrf import csrf_protect
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from getchapp.models import Post, Brand, Profile, Item, Tag, Comment
from .forms import PostForm, TagForm


brands_all = Brand.objects.all()
items_all = Item.objects.all()
brands_search = list(brands_all.values('pk', 'name', 'image', 'category', 'fullname_kr', 'fullname_en', 'keywords').order_by('name'))
items_search = list(items_all.values('pk', 'name', 'image', 'keywords').order_by('name'))


def intro(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'getchapp/intro.html', {'posts':posts})

# @login_required
def posting(request):
    if request.method=='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = get_object_or_404(Profile, user=request.user)
            obj.save()
            return redirect(obj)

    else:
        form = PostForm()
        return render(request, 'getchapp/posting.html', {'form':form})


def my(request):
    return render(request, 'getchapp/my.html')


# @csrf_protect
def save_tag(request, pk):
    resp_fail = JsonResponse({'success':False})

    if request.method=='POST':
        try:
            tagform = TagForm(request.POST, request.FILES)
            if tagform.is_valid():
                obj = tagform.save(commit=False)
                obj.on_id = pk
                obj.x = request.POST['x']
                obj.y = request.POST['y']
                obj.brand_id = request.POST['brand_id']
                obj.item_id = request.POST['item_id']
                obj.author = get_object_or_404(Profile, user=request.user)
                obj.save()

                # _tags = serializers.serialize('python', Tag.objects.filter(on__pk=pk), use_natural_foreign_keys=True)
                # return JsonResponse({'success':True, 'tags':_tags}, safe=False)
                _tags = Tag.objects.filter(on__pk=pk).values('pk', 'x', 'y', 'brand__image', 'item__image')
                return JsonResponse({'success':True, 'tags':list(_tags)}, safe=False)

            else:
                return resp_fail

        except:
            return resp_fail

    else:
        return resp_fail


def tag_feed(request, pk):
    resp_fail = JsonResponse({'success':False})

    if request.method=='GET':
        tag = serializers.serialize('python', Tag.objects.filter(pk=pk), use_natural_foreign_keys=True)[0]
        comments = Comment.objects.filter(content_type__model='tag', object_id=pk).values()
        return JsonResponse({'success':True, 'tag':tag, 'comments':list(comments)}, safe=False)



def post(request, pk):
    _post = get_object_or_404(Post, pk=pk)
    _tagform = TagForm()
    ctx = {'post':_post, 'brands':brands_search, 'items':items_search, 'tagform':_tagform}

    if request.method=='POST':
        print('*******************************')
        pass
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

    else:
        return render(request, 'getchapp/post.html', ctx)



def brand(request, pk):
    _brand = get_object_or_404(Brand, pk=pk)
    return render(request, 'getchapp/brand.html', {'brand':_brand})


def item(request, pk):
    _item = get_object_or_404(Item, pk=pk)
    return render(request, 'getchapp/item.html', {'item':_item})


def profile(request, pk):
    _profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'getchapp/profile.html', {'profile':_profile})
