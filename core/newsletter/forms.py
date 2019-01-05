from django import forms
from django.utils.text import slugify
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'description'
        ]