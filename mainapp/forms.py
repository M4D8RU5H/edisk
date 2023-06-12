from django import forms
from multiupload.fields import MultiFileField

class MyfileUploadForm(forms.Form):
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    files_data = MultiFileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

