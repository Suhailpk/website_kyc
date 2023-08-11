from django import forms
from .models import Ann_table


class AnnTableForm(forms.ModelForm):
    class Meta:
        model = Ann_table
        fields = '__all__'