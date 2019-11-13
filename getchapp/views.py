from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.

def intro(request):
    return render(request, 'getchapp/intro.html')

def posting(request):
    #eturn render(request, 'getchapp/posting.html')
    return HttpResponse('posting')

def my(request):
    #return render(request, 'getchapp/my.html')
    return HttpResponse('my')
