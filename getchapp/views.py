from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from getchapp.models import Post, Brand


# Create your views here.

def intro(request):
    posts = Post.objects.all()
    return render(request, 'getchapp/intro.html', {'posts':posts})

def posting(request):
    #eturn render(request, 'getchapp/posting.html')
    return HttpResponse('posting')

def my(request):
    return render(request, 'getchapp/my.html')


def post(request, pk):
    _post = get_object_or_404(Post, pk=pk)
    _brands = Brand.objects.all().values('name', 'image', 'category', 'fullname_kr', 'fullname_en', 'keywords').order_by('name')
    return render(request, 'getchapp/post.html', {'post':_post, 'brands':list(_brands)})
