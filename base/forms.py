from django import forms
from .models import Kyc


class EmailForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class KycForm(forms.ModelForm):
    class Meta:
        model = Kyc
        fields = '__all__'
        exclude = ['approved', 'waiting', 'user','submitted']
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'nationality': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'passport': forms.FileInput(attrs={'class':'form-control'}),
            'aadhaar': forms.FileInput(attrs={'class':'form-control'}),
            'driving_license': forms.FileInput(attrs={'class':'form-control'}),
        }





    

        




