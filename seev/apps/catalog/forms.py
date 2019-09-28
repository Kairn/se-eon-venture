"""
Form definitions for catalog app
"""

from django import forms


class AddPrForm(forms.Form):
    product_code = forms.CharField(
        required=True,
        label='Product Code',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Product Code',
                'maxlength': '32'
            }
        )
    )

    product_name = forms.CharField(
        required=True,
        label='Product Name',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Product Name',
                'maxlength': '128'
            }
        )
    )


class editPrForm(forms.Form):
    product_code = forms.CharField(
        label='Product Code',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Product Code',
                'maxlength': '32',
                'disabled': 'true',
                'class': 'form-inp-dis'
            }
        )
    )

    product_name = forms.CharField(
        required=True,
        label='Product Name',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Product Name',
                'maxlength': '128'
            }
        )
    )
