from django import forms


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
        label='Email',
        label_suffix='',
        error_messages={
            'required': 'Email address is required',
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
            'required': 'PIN number is required',
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
