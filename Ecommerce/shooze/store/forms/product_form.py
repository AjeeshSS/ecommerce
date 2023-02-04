from django import forms
from store.models.product import Product


class Product_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stoke', 'description','brand', 'image', 'category']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),

        }