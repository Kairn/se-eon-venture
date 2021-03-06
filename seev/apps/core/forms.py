"""
Form definitions for core app
"""

from django import forms

from seev.apps.utils.country import UnoCountry
from seev.apps.utils.state import UnoState


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        label_suffix='',
        error_messages={
            'required': 'Please enter your username',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
            }
        )
    )

    password = forms.CharField(
        required=True,
        label='Password',
        label_suffix='',
        error_messages={
            'required': 'Please enter your password',
        },
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        )
    )


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Recovery Email',
        label_suffix='',
        error_messages={
            'required': 'Please enter your recovery email',
        },
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
            }
        )
    )

    pin = forms.IntegerField(
        required=True,
        label='PIN',
        label_suffix='',
        max_value=9999,
        min_value=1000,
        error_messages={
            'required': 'Please enter your PIN',
            'invalid': 'Enter a valid PIN number',
            'max_value': 'Enter a valid PIN number',
            'min_value': 'Enter a valid PIN number',
        },
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'PIN',
            }
        )
    )


class RegisterForm(forms.Form):
    entity_name = forms.CharField(
        required=True,
        label='Entity Name',
        label_suffix='',
        error_messages={
            'required': 'Entity name is required',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Entity name',
            }
        )
    )

    country = forms.ChoiceField(
        required=True,
        label='Country',
        label_suffix='',
        error_messages={
            'required': 'Country is required',
        },
        choices=UnoCountry.get_cty_code_list
    )

    trade_ticker = forms.CharField(
        required=False,
        label='Trade Symbol',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'e.g. AAPL',
            }
        )
    )

    contact_email = forms.EmailField(
        required=True,
        label='Contact Email',
        label_suffix='',
        error_messages={
            'required': 'Contact email is required',
        },
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Contact email',
            }
        )
    )

    contact_phone = forms.CharField(
        required=True,
        label='Contact Phone',
        label_suffix='',
        error_messages={
            'required': 'Contact phone is required',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'e.g. 123-456-7890',
            }
        )
    )

    summary = forms.CharField(
        required=False,
        label='Business Summary',
        label_suffix='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Business summary',
                'maxlength': 1000,
            }
        )
    )

    website = forms.CharField(
        required=False,
        label='Website',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'e.g. www.example.com',
            }
        )
    )

    signature_letter = forms.FileField(
        required=False,
        label='Signed Request Letter (Deprecated)',
        label_suffix='',
        allow_empty_file=False,
        widget=forms.FileInput()
    )

    username = forms.CharField(
        required=True,
        label='Create Username',
        label_suffix='',
        error_messages={
            'required': 'Username is required',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
            }
        )
    )

    password = forms.CharField(
        required=True,
        label='Create Password',
        label_suffix='',
        error_messages={
            'required': 'Password is required',
        },
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        )
    )

    confirm_password = forms.CharField(
        required=True,
        label='Confirm Password',
        label_suffix='',
        error_messages={
            'required': 'Please re-type your password',
        },
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password again',
            }
        )
    )

    recovery_email = forms.EmailField(
        required=True,
        label='Recovery Email',
        label_suffix='',
        error_messages={
            'required': 'Recovery email is required',
        },
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Recovery email',
            }
        )
    )

    pin = forms.IntegerField(
        required=True,
        label='PIN',
        label_suffix='',
        error_messages={
            'required': 'PIN number is required',
        },
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'PIN',
            }
        )
    )


class ApprovalForm(forms.Form):
    client_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

    action = forms.ChoiceField(
        required=True,
        label='Action',
        label_suffix='',
        error_messages={
            'required': 'Action is required',
        },
        choices=[
            ('AP', 'Approve'),
            ('DE', 'Deny'),
            ('RV', 'Revoke'),
            ('RI', 'Reinstate'),
        ]
    )

    message = forms.CharField(
        required=False,
        label='Comment',
        label_suffix='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Write your justification here',
                'rows': 5,
                'maxlength': 300,
            }
        )
    )


class CustomerForm(forms.Form):
    customer_name = forms.CharField(
        required=True,
        label='Customer Name',
        label_suffix='',
        error_messages={
            'required': 'Customer name is required',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Customer name',
            }
        )
    )

    country = forms.ChoiceField(
        required=True,
        label='Country',
        label_suffix='',
        error_messages={
            'required': 'Country is required',
        },
        choices=UnoCountry.get_cty_code_list
    )

    contact_email = forms.EmailField(
        required=True,
        label='Contact Email',
        label_suffix='',
        error_messages={
            'required': 'Contact email is required',
        },
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Contact email',
            }
        )
    )


class OpportunityForm(forms.Form):
    client_id = forms.CharField(
        label=None,
        label_suffix=None,
        widget=forms.HiddenInput()
    )

    customer = forms.ChoiceField(
        required=True,
        label='Customer',
        label_suffix='',
        error_messages={
            'required': 'Customer is required',
        },
        choices=[]
    )

    discount_nrc = forms.ChoiceField(
        required=False,
        label='Non-recurring Discount',
        label_suffix='',
        choices=[
            ('0', 'No Discount'),
            ('5', '5% Discount'),
            ('10', '10% Discount'),
            ('15', '15% Discount'),
            ('20', '20% Discount'),
            ('25', '25% Discount'),
            ('30', '30% Discount'),
        ]
    )

    discount_mrc = forms.ChoiceField(
        required=False,
        label='Monthly Discount',
        label_suffix='',
        choices=[
            ('0', 'No Discount'),
            ('5', '5% Discount'),
            ('10', '10% Discount'),
            ('15', '15% Discount'),
            ('20', '20% Discount'),
            ('25', '25% Discount'),
            ('30', '30% Discount'),
        ]
    )

    deal_limit = forms.IntegerField(
        required=True,
        label='Deal Limit',
        label_suffix='',
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Maximum orders',
            }
        )
    )
