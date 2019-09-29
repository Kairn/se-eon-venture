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


class EditPrForm(forms.Form):
    product_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

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
