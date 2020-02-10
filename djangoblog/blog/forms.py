from django import forms
from .models import Post
from django.contrib.auth.models import User


class AddBlog(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.Textarea()

    class Meta:
        model = Post
        fields = ['title', 'content', 'author']


class EditBlog(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class GetPost(forms.ModelForm):
    class Meta:
        models = Post
        fields = ['title', 'content']