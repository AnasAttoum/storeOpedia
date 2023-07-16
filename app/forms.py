from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Post
        fields = ('photos','title','description','category','price')
        # fields = '__all__'
        labels={
            'photos':'',
            'title':'',
            'description':'',
            'category':'',
            'price':'',
        }