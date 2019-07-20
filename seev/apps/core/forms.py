from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        error_messages={
            'required': 'Please enter your username',
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-ti-field',
                'placeholder': 'Username',
            }
        )
    )
    password = forms.CharField(
        required=True,
        label='Password',
        error_messages={
            'required': 'Please enter your password',
        },
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-ti-field',
                'placeholder': 'Password',
            }
        )
    )


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Email',
        error_messages={
            'required': 'Email address is required',
        },
        widget=forms.EmailInput(
            attrs={
                'class': 'form-ti-field',
                'placeholder': 'Email',
            }
        )
    )
    pin = forms.IntegerField(
        required=True,
        label='PIN',
        max_value=9999,
        min_value=1000,
        error_messages={
            'required': 'PIN number is required',
            'invalid': 'Enter a valid PIN number',
        },
        widget=forms.NumberInput(
            attrs={
                'class': 'form-ti-field',
                'placeholder': 'PIN',
            }
        )
    )
