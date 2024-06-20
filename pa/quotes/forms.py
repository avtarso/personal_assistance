from django import forms

from .models import Author, Quote, Tag


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]
        labels = {
            "fullname": "Aythor`s Full Name",
            "born_date": "Date of Birth",
            "born_location": "Place of Birth",
            "description": "Description",
        }
        help_texts = {
            "fullname": "<--- Enter the full name of the author.",
            "born_date": "<--- Enter the birth date in the format YYYY-MM-DD.",
            "born_location": "<--- Enter the location where the author was born.",
            "description": "<--- Enter a brief description or biography of the author.",
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "author", "tags"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "cols": 40}),
            "author": forms.Select(),
            "tags": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "text": "Quote",
            "author": "Author",
            "tags": "Tags",
        }
        help_texts = {
            "text": "<--- Enter the quote",
            "author": "<--- Select author",
            "tags": "Select tags ",
        }


class UploadFileForm(forms.Form):
    file = forms.FileField()
