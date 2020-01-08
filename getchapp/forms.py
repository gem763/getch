from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('pix', 'text', )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('pix', 'text', )


            # target = models.ForeignKey('Pix', on_delete=models.CASCADE)
            # x = models.FloatField(default=0)
            # y = models.FloatField(default=0)
            # with_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
            # with_item = models.ForeignKey(Item, on_delete=models.CASCADE)
