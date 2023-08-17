from django import forms
from .models import Ann_table


class AnnTableForm(forms.ModelForm):
    class Meta:
        model = Ann_table
        fields = '__all__'
        widgets = {
            'subject': forms.TextInput(attrs={'class':'form-control'}),
            'message': forms.TextInput(attrs={'class':'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'datepicker2'}),
        }