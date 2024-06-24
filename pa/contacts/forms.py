from django import forms

from .models import Contact


class NoteForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "address", "phone", "email", "birthday"]
        labels = {
            "name": "Name",
            "address": "Address",
            "phone": "Phone",
            "email": "Email",
            "birthday": "Birthday"
        }