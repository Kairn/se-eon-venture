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
        required=True,
        label='Signed Request Letter',
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
