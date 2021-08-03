from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from django.http import HttpResponse



class WriteAPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def clean_content(self):
        data = self.cleaned_data["content"]
        if "hack" in data:
            raise ValidationError("This word is not admitted in this site")
        return data





