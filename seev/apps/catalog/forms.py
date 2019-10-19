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


class EditSpecForm(forms.Form):
    specification_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

    leaf_name = forms.CharField(
        required=False,
        label='Specification Code',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Specification Code',
                'maxlength': '32',
                'disabled': 'true',
                'class': 'form-inp-dis'
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

    data_type = forms.CharField(
        required=False,
        label='Data Type',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'disabled': 'true',
                'class': 'form-inp-dis'
            }
        )
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


class AddValueForm(forms.Form):
    specification_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

    code = forms.CharField(
        required=True,
        label='Code Name',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Code Name',
                'maxlength': '32'
            }
        )
    )

    translation = forms.CharField(
        required=True,
        label='Code Translation',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Code Translation',
                'maxlength': '128'
            }
        )
    )


class RestrictionForm(forms.Form):
    specification_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

    max_val = forms.CharField(
        required=False,
        label='Maximum Value',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Maximum Value',
                'maxlength': '32'
            }
        )
    )

    min_val = forms.CharField(
        required=False,
        label='Minimum Value',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Minimum Value',
                'maxlength': '32'
            }
        )
    )

    max_len = forms.CharField(
        required=False,
        label='Maximum Length',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Maximum Length',
                'maxlength': '32'
            }
        )
    )

    min_len = forms.CharField(
        required=False,
        label='Minimum Length',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Minimum Length',
                'maxlength': '32'
            }
        )
    )

    alpha_only = forms.ChoiceField(
        required=False,
        label='Letters Only',
        label_suffix='',
        choices=[
            ('N', 'No'),
            ('Y', 'Yes'),
        ]
    )

    num_only = forms.ChoiceField(
        required=False,
        label='Numbers Only',
        label_suffix='',
        choices=[
            ('N', 'No'),
            ('Y', 'Yes'),
        ]
    )

    email_only = forms.ChoiceField(
        required=False,
        label='Email Format',
        label_suffix='',
        choices=[
            ('N', 'No'),
            ('Y', 'Yes'),
        ]
    )

    not_null = forms.ChoiceField(
        required=True,
        label='Required',
        label_suffix='',
        choices=[
            ('N', 'No'),
            ('Y', 'Yes'),
        ]
    )


class PriceForm(forms.Form):
    specification_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

    mrc = forms.CharField(
        required=False,
        label='Monthly Charge',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '0.00',
                'maxlength': '16'
            }
        )
    )

    nrc = forms.CharField(
        required=False,
        label='Non-recurring Charge',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '0.00',
                'maxlength': '16'
            }
        )
    )

    unit_mrc = forms.CharField(
        required=False,
        label='Unit Monthly Charge',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '0.00',
                'maxlength': '16'
            }
        )
    )

    unit_nrc = forms.CharField(
        required=False,
        label='Unit Charge',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '0.00',
                'maxlength': '16'
            }
        )
    )

    value = forms.ChoiceField(
        required=False,
        label='Specification Value',
        label_suffix='',
        choices=[]
    )
