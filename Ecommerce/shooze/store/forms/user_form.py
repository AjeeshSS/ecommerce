from django import forms
from store.models.our_user import Our_user


class user_form(forms.ModelForm):
    class Meta:
        model = Our_user
        fields = ['name', 'address', 'pincode', 'phone','email', 'landmark']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control'}),

        }