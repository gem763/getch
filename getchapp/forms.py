from django import forms
from .models import Post, Tag


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('image', 'text', )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('image', 'text', )
