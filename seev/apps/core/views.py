from django.shortcuts import render, redirect

from seev.apps.utils.generators import getRandomSalt, getSha384Hash
from seev.apps.utils.validations import isValidRegisterRequest

from .models import UnoClient, UnoCredentials
from .forms import LoginForm, PasswordResetForm, RegisterForm

# Create your views here.


def go_landing(request):
    request.session.set_test_cookie()

    context = {}
    return render(request, 'core/index.html', context=context)


def go_login(request):
    if request.session.test_cookie_worked():
        print('Django session is working')
        request.session.delete_test_cookie()

    context = {}
    if request.method == 'GET':
        loginForm = LoginForm()
        psrForm = PasswordResetForm()
        context['loginForm'] = loginForm
        context['psrForm'] = psrForm

    return render(request, 'core/login.html', context=context)


def auth_login(request):
    if request.method == 'POST':
        return redirect('go_landing')
    else:
        return redirect('go_login')


def auth_password_reset(request):
    if request.method == 'POST':
        return redirect('go_landing')
    else:
        return redirect('go_login')


def go_register(request):
    context = {}
    if request.method == 'GET':
        registerForm = RegisterForm()
        context['registerForm'] = registerForm

    return render(request, 'core/register.html', context=context)


def do_register(request):
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST, request.FILES)

        # Basic validation
        if registerForm.is_multipart() and registerForm.is_valid():
            # Specific validation
            if isValidRegisterRequest(request.POST):
                entity_name = request.POST['entity_name']
                country = request.POST['country']
                trade_ticker = request.POST['trade_ticker']
                contact_email = request.POST['contact_email']
                contact_phone = request.POST['contact_phone']
                summary = request.POST['summary']
                website = request.POST['website']
                username = request.POST['username']
                password = request.POST['password']
                recovery_email = request.POST['recovery_email']
                pin = request.POST['pin']

                signature_letter = request.FILES['signature_letter']
                sl_bin = b''

                password_salt = getRandomSalt(8)

                # Obtain binary data
                for chunk in signature_letter.chunks():
                    sl_bin += chunk

                if len(trade_ticker) == 0:
                    trade_ticker = None
                if len(summary) == 0:
                    summary = None
                if len(website) == 0:
                    website = None

                print(UnoClient(
                    ctg_name=None,
                    entity_name=entity_name,
                    country=country,
                    trade_ticker=trade_ticker,
                    contact_email=contact_email,
                    contact_phone=contact_phone,
                    signature_letter=sl_bin,
                    summary=summary,
                    website=website
                ).__dict__)

                print(UnoCredentials(
                    client=None,
                    username=username,
                    password_salt=password_salt,
                    password_hash=getSha384Hash(password + password_salt),
                    recovery_email=recovery_email,
                    pin=pin
                ).__dict__)

                return go_success(None, {'message': 'We will be working hard to process your request.'})
            else:
                return redirect('go_register')
        else:
            return redirect('go_register')
    else:
        return redirect('go_register')


def go_success(request, context):
    context = context
    return render(request, 'core/success.html', context=context)
