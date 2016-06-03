from catalog.models import Libraries
from django import forms


class LibrariesForm(forms.ModelForm):
    class Meta:
        model = Libraries
        fields = ['name', 'image']
