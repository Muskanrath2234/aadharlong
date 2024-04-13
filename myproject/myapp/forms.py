from django import forms

class AadharImageForm_long(forms.Form):
    aadhar_image_long = forms.ImageField(label='Upload Aadhar Image')
