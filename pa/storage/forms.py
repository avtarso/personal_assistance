# storage/forms.py
from django import forms
from django.conf import settings


from .models import UploadedFile, FileTag

class FileTagForm(forms.ModelForm):
    class Meta:
        model = FileTag
        fields = ["name"]
    

class FileUploadForm(forms.ModelForm):
    file = forms.FileField(required=True)

    class Meta:
        model = UploadedFile
        fields = ['description', 'tags', 'attention_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'tags': forms.SelectMultiple(),
            'attention_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'description': 'File description',
            'tags': 'Tags',
            'attention_date': 'Date for review',
        }
        help_texts = {
            'description': '<--- Enter the description',
            'tags': '<--- Select tags',
            'attention_date': '<--- Enter attention_date',
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file and uploaded_file.size > settings.MAX_FILE_SIZE:
            raise forms.ValidationError(f"File size exceeds {settings.MAX_FILE_SIZE / (1024 * 1024):.2f} Mb")
        return uploaded_file
    

class UploadedFileEditForm(forms.ModelForm):
    attention_date = forms.DateField(required=False,
        widget=forms.DateInput(attrs={'type': 'date'}))
    tags = forms.ModelMultipleChoiceField(queryset=FileTag.objects.all(),
        widget=forms.CheckboxSelectMultiple, required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = UploadedFile
        fields = ['attention_date', 'tags', 'description']
