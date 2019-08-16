"""
View logic used in core app
"""

import traceback

from django.http import HttpRequest
from django.db import transaction
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from seev.apps.utils.generators import (getRandomSalt, getSha384Hash,
                                        getSha224Hash, getAdminCredentials, getCpAdminId)
from seev.apps.utils.validations import isValidRegisterRequest
from seev.apps.utils.messages import get_app_message

from .models import UnoClient, UnoCredentials
from .forms import LoginForm, PasswordResetForm, RegisterForm, ApprovalForm

# Create your views here.


def go_landing(request):
    request.session.set_test_cookie()

    context = {}
    return render(request, 'core/index.html', context=context)


def go_login(request, context=None):
    if request and request.session.test_cookie_worked():
        print('Django session is working')
        request.session.delete_test_cookie()

    context = context
    if context is None:
        context = {}

    if request.method == 'GET':
        loginForm = LoginForm()
        psrForm = PasswordResetForm()
        context['loginForm'] = loginForm
        context['psrForm'] = psrForm

    return render(request, 'core/login.html', context=context)


def auth_login(request):
    if request.method == 'POST':
        try:
            unHash = getSha224Hash(request.POST['username'])
            psHash = getSha224Hash(request.POST['password'])

            if unHash == getAdminCredentials()[0] and psHash == getAdminCredentials()[1]:
                request.session['id'] = getCpAdminId()
                return redirect('go_admin')
            else:
                request.session.clear()
                return redirect('go_login')
        except RuntimeError:
            traceback.print_exc()
            request.session.clear()
            return redirect('go_login')
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


@transaction.atomic
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

                try:
                    # Create client object
                    newClient = UnoClient(
                        ctg_name=None,
                        entity_name=entity_name,
                        country=country,
                        trade_ticker=trade_ticker,
                        contact_email=contact_email,
                        contact_phone=contact_phone,
                        signature_letter=sl_bin,
                        summary=summary,
                        website=website
                    )

                    # Create credentials object
                    newCredentials = UnoCredentials(
                        client=newClient,
                        username=username,
                        password_salt=password_salt,
                        password_hash=getSha384Hash(password + password_salt),
                        recovery_email=recovery_email,
                        pin=pin
                    )

                    newClient.save()
                    newCredentials.save()
                except RuntimeError:
                    traceback.print_exc()
                    return go_error(HttpRequest(), {'error': get_app_message('register_error'), 'message': get_app_message('register_error_message')})

                return go_success(HttpRequest(), {'message': get_app_message('register_success')})
            else:
                return go_error(HttpRequest(), {'error': get_app_message('register_error'), 'message': get_app_message('register_error_message')})
        else:
            return go_error(HttpRequest(), {'error': get_app_message('register_error'), 'message': get_app_message('register_error_message')})
    else:
        return redirect('go_register')


def go_success(request, context):
    context = context
    return render(request, 'core/success.html', context=context)


def go_error(request, context):
    context = context
    return render(request, 'core/error.html', context=context)


def go_admin(request, context=None):
    try:
        if request is None:
            return redirect('go_login')
        elif request.session['id'] != getCpAdminId():
            request.session.clear()
            return redirect('go_login')
    except KeyError:
        return redirect('go_login')

    context = context
    if context is None:
        context = {}

    ITEMS_PER_PAGE = 3

    requestPage = None
    if request.GET.get('request_page'):
        requestPage = request.GET.get('request_page')
    else:
        requestPage = 1

    # Fetch client data
    clientList = UnoClient.objects.all().order_by('-creation_time', 'client_id')
    pagedList = Paginator(clientList, ITEMS_PER_PAGE)
    clients = pagedList.get_page(requestPage)

    for client in clients:
        tempBytes = client.signature_letter
        if tempBytes:
            client.signature_letter = tempBytes.decode('U8')

    context['clients'] = clients
    context['approvalForm'] = ApprovalForm()

    return render(request, 'core/admin.html', context=context)


def go_logout(request):
    if request:
        request.session.clear()

    return redirect('go_landing')
