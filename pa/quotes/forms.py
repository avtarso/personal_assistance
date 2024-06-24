from django import forms

from .models import Author, Quote


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


class UploadFileForm(forms.Form):
    file = forms.FileField()
