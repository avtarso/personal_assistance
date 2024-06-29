from django import forms

from .models import Contact
from .validators import EmailValidator, NameValidator, PhoneValidator, BirthdayValidator


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=30,
        required=True,
        validators=[NameValidator()]
    )
    address = forms.CharField(
        max_length=100,
        required=False
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        validators=[PhoneValidator()]
    )
    email = forms.CharField(
        max_length=50,
        required=False,
        validators=[EmailValidator()]
    )
    birthday = forms.DateField(
        required=False,
        validators=[BirthdayValidator()],
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Contact
        fields = ["name", "address", "phone", "email", "birthday"]
        exclude = ["added_by"]
