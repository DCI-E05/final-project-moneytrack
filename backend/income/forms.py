from django import forms

class DocUploadForm(forms.Form):
    receipt_image = forms.ImageField(
        label='Upload a Document or take a photo',
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*', 'capture': 'camera'})
    )
