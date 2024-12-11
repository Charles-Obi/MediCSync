from django import forms
from myapp.models import Appointment1, ImageModel

class Appointment1Form(forms.ModelForm):
    class Meta:
        model = Appointment1
        fields = '__all__'

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = '__all__'

