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
        required=False,
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


class AddSpecForm(forms.Form):
    parent_ctg_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

    leaf_name = forms.CharField(
        required=True,
        label='Specification Code',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Specification Code',
                'maxlength': '32'
            }
        )
    )

    spec_label = forms.CharField(
        required=True,
        label='Specification Name',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Specification Name',
                'maxlength': '128'
            }
        )
    )

    data_type = forms.ChoiceField(
        required=True,
        label='Specification Type',
        label_suffix='',
        choices=[
            ('BO', 'Boolean'),
            ('STR', 'String'),
            ('QTY', 'Quantity'),
            ('ENUM', 'Enumeration'),
        ]
    )

    default_value = forms.CharField(
        required=False,
        label='Default Value',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Default Value',
                'maxlength': '512'
            }
        )
    )


class AddFetForm(forms.Form):
    product_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

    feature_code = forms.CharField(
        required=True,
        label='Feature Code',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Feature Code',
                'maxlength': '32'
            }
        )
    )

    feature_name = forms.CharField(
        required=True,
        label='Feature Name',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Feature Name',
                'maxlength': '128'
            }
        )
    )

    limit = forms.IntegerField(
        required=False,
        label='Limit',
        widget=forms.TextInput(
            attrs={
                'placeholder': '1'
            }
        )
    )

    is_extended = forms.ChoiceField(
        required=True,
        label='Extended Only',
        label_suffix='',
        choices=[
            ('N', 'No'),
            ('Y', 'Yes'),
        ]
    )


class EditFetForm(forms.Form):
    feature_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

    feature_code = forms.CharField(
        required=False,
        label='Feature Code',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Feature Code',
                'maxlength': '32',
                'disabled': 'true',
                'class': 'form-inp-dis'
            }
        )
    )

    feature_name = forms.CharField(
        required=True,
        label='Feature Name',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Feature Name',
                'maxlength': '128'
            }
        )
    )

    limit = forms.IntegerField(
        required=False,
        label='Limit',
        widget=forms.TextInput(
            attrs={
                'placeholder': '1'
            }
        )
    )

    is_extended = forms.ChoiceField(
        required=True,
        label='Extended Only',
        label_suffix='',
        choices=[
            ('N', 'No'),
            ('Y', 'Yes'),
        ]
    )
