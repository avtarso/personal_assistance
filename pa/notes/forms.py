from django import forms

from .models import Note, Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["name", "description", "tags"]
        labels = {
            "name": "Note`s short name",
            "description": "Note`s description",
            "tags": "Tags"
        }