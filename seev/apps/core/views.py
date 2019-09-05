"""
View logic used in core app
"""

import traceback

from django.conf import settings
from django.http import HttpRequest
from django.db import transaction
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator

from seev.apps.utils.generators import (getRandomSalt, getSha384Hash,
                                        getSha224Hash, getAdminCredentials, getCpAdminId,
                                        getClientStates)
from seev.apps.utils.validations import isValidRegisterRequest
from seev.apps.utils.messages import get_app_message, addSnackDataToContext, getNewOppoMessage
from seev.apps.utils.session import store_context_in_session, get_context_in_session

from .models import UnoClient, UnoCredentials, UnoApproval, UnoCustomer, UnoOpportunity
from .forms import (LoginForm, PasswordResetForm, RegisterForm,
                    ApprovalForm, CustomerForm, OpportunityForm)

# Create your views here.


def go_landing(request):
    request.session.set_test_cookie()

    context = {}
    return render(request, 'core/index.html', context=context)


def go_login(request, context=None):
    try:
        if request and request.session and request.session.test_cookie_worked():
            print('Django session is working')
            request.session.delete_test_cookie()
    except AttributeError:
        pass

    # Retrieve session context if passed
    context = get_context_in_session(request)

    if context is None:
        context = {}

    if request.method == 'GET':
        loginForm = LoginForm()
        psrForm = PasswordResetForm()
        context['loginForm'] = loginForm
        context['psrForm'] = psrForm

    return render(request, 'core/login.html', context=context)


def auth_login(request):
    context = {}

    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            unHash = getSha224Hash(username)
            psHash = getSha224Hash(password)

            if unHash == getAdminCredentials()[0] and psHash == getAdminCredentials()[1]:
                request.session['id'] = getCpAdminId()
                return redirect('go_admin')

            # Get client credentials data
            credObj = UnoCredentials.objects.get(username=username)

            if credObj and credObj.password_hash == getSha384Hash(password + credObj.password_salt):
                client = UnoClient.objects.get(client_id=credObj.client_id)

                if client.active:
                    request.session['id'] = str(
                        credObj.client_id).replace('-', '')
                    return redirect('go_client')
                else:
                    store_context_in_session(
                        request, addSnackDataToContext(context, 'Access denied'))
                    return redirect('go_login')
            else:
                request.session.clear()
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Invalid credentials'))
                return redirect('go_login')
        except Exception:
            traceback.print_exc()
            request.session.clear()
            store_context_in_session(
                request, addSnackDataToContext(context, 'ERR01'))
            return redirect('go_login')
    else:
        store_context_in_session(
            request, addSnackDataToContext(context, 'ERR01'))
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

                # Obtain binary data (deprecated but doable)
                sl_bin = b''
                try:
                    signature_letter = request.FILES['signature_letter']
                    for chunk in signature_letter.chunks():
                        sl_bin += chunk
                except KeyError:
                    sl_bin = b''
                    pass

                password_salt = getRandomSalt(8)

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
                except Exception:
                    traceback.print_exc()
                    return go_error(HttpRequest(), {'error': get_app_message('register_error'), 'message': get_app_message('register_error_message')})

                return go_success(HttpRequest(), {'message': get_app_message('register_success')})
            else:
                return go_error(HttpRequest(), {'error': get_app_message('register_error'), 'message': get_app_message('register_error_message')})
        else:
            return go_error(HttpRequest(), {'error': get_app_message('register_error'), 'message': get_app_message('register_error_message')})
    else:
        return redirect('go_register')


def go_success(request, context=None):
    context = context

    if not context and not settings.DEBUG:
        return redirect('go_landing')

    if context is None:
        context = {}

    if 'return_link' in context:
        pass
    else:
        context['return_link'] = reverse('go_landing')

    return render(request, 'core/success.html', context=context)


def go_error(request, context=None):
    context = context

    if not context and not settings.DEBUG:
        return redirect('go_landing')

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

    context = get_context_in_session(request)

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

    # Store the current page in temp session variable
    request.session['admin_page'] = requestPage

    # Deprecated but usable
    for client in clients:
        tempBytes = client.signature_letter
        if tempBytes:
            client.signature_letter = tempBytes.decode('U8')

    context['clients'] = clients
    context['approvalForm'] = ApprovalForm()

    return render(request, 'core/admin.html', context=context)


def go_logout(request):
    if request and hasattr(request, 'session') and request.session:
        request.session.clear()

    return redirect('go_landing')


@transaction.atomic
def do_approve(request):
    if request.method == 'POST':
        try:
            if request.session['id'] != getCpAdminId():
                request.session.clear()
                return redirect('go_login')

            # Retrieve form data
            client_id = request.POST['client_id']
            ctg_name = request.POST['ctg_name']
            action = request.POST['action']
            comment = request.POST['message']

            # Get client data
            client = UnoClient.objects.get(client_id=client_id)

            # Validate action
            valid = False
            tempStatus = ''
            if client.status == getClientStates('PE'):
                if action == 'AP' and ctg_name:
                    valid = True
                    tempStatus = getClientStates('AP')
                elif action == 'DE':
                    valid = True
                    tempStatus = getClientStates('DE')
            elif client.status == getClientStates('AP'):
                if action == 'RV':
                    valid = True
                    tempStatus = getClientStates('RV')
            elif client.status == getClientStates('RV'):
                if action == 'RI':
                    valid = True
                    tempStatus = getClientStates('AP')
            else:
                valid = False

            if not valid:
                raise RuntimeError

            # Create approval data
            newApproval = UnoApproval(
                client=client,
                action=action,
                message=comment
            )
            newApproval.save()

            # Update client data
            if (tempStatus == getClientStates('AP')):
                client.active = 1
                client.ctg_name = ctg_name
            else:
                client.active = 0
            client.status = tempStatus
            client.save()

            # Retrieve the current page
            redirectPage = 1
            if 'admin_page' in request.session:
                redirectPage = request.session['admin_page']

            # Success message
            store_context_in_session(request, addSnackDataToContext(
                {}, 'Your action has been applied'))

            return redirect(reverse('go_admin') + '?request_page=' + str(redirectPage))
        except Exception:
            traceback.print_exc()
            return go_error(HttpRequest(), {'error': get_app_message('approval_error'), 'message': get_app_message('approval_error_message')})
    else:
        return redirect('go_admin')


def go_client(request, context=None):
    if request and hasattr(request, 'session') and request.session and 'id' in request.session:
        if len(request.session['id']) != 32:
            request.session.clear()
            return redirect('go_login')
        else:
            context = get_context_in_session(request)

            if context is None:
                context = {}

            client = UnoClient.objects.get(client_id=request.session['id'])
            context['client'] = client

            # Customer form
            context['customerForm'] = CustomerForm()

            # Opportunity form
            oppoForm = OpportunityForm(initial={'client_id': client.client_id})

            customerList = UnoCustomer.objects.filter(client=client)
            custChoice = []

            for cust in customerList:
                choice = (cust.customer_id, cust.customer_name)
                custChoice.append(choice)

            if len(custChoice) > 0:
                oppoForm.fields['customer'].choices = custChoice
                context['oppoForm'] = oppoForm
            else:
                context['oppoForm'] = None

            return render(request, 'core/client.html', context=context)
    else:
        return redirect('go_login')


@transaction.atomic
def do_enroll(request):
    if request and request.method == 'POST':
        try:
            context = {}

            # Verify client
            client = None
            if request.session:
                client = UnoClient.objects.get(client_id=request.session['id'])

            if not client:
                raise RuntimeError

            # Retrieve form values
            customer_name = request.POST['customer_name']
            contact_email = request.POST['contact_email']
            country = request.POST['country']

            if customer_name and contact_email and country:
                newCustomer = UnoCustomer(
                    client=client,
                    customer_name=customer_name,
                    contact_email=contact_email,
                    country=country
                )

                newCustomer.save()
                return go_success(HttpRequest(), {'message': get_app_message('enroll_success'), 'return_link': reverse('go_client')})
            else:
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Invalid form data'))
            return redirect('go_login')
        except RuntimeError:
            if hasattr(request, 'session') and request.session:
                request.session.clear()

            store_context_in_session(request, addSnackDataToContext(
                context, 'Invalid client session'))
            return redirect('go_login')
        except Exception:
            traceback.print_exc()
            return go_error(HttpRequest(), {'error': get_app_message('enroll_error'), 'message': get_app_message('enroll_error_message')})
    else:
        return redirect('go_client')


@transaction.atomic
def do_oppo(request, context=None):
    if request and request.method == 'POST':
        try:
            if not context:
                context = {}

            client = None
            if request.session:
                client = UnoClient.objects.get(client_id=request.session['id'])

            if not client:
                raise RuntimeError

            # Get opportunity details
            customer_id = request.POST['customer']
            discount_nrc = request.POST['discount_nrc']
            discount_mrc = request.POST['discount_mrc']
            deal_limit = int(request.POST['deal_limit'])

            if deal_limit < 1 or deal_limit > 32:
                raise AssertionError

            customer_id = str(customer_id).replace('-', '')
            customer = UnoCustomer.objects.get(customer_id=customer_id)

            newOpportunity = UnoOpportunity(
                client=client,
                customer=customer,
                discount_nrc=discount_nrc,
                discount_mrc=discount_mrc,
                deal_limit=deal_limit
            )

            newOpportunity.save()
            return go_success(HttpRequest(), {'message': getNewOppoMessage(newOpportunity.opportunity_number), 'return_link': reverse('go_client')})
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Invalid data encountered'))
            return redirect('go_client')
        except RuntimeError:
            if hasattr(request, 'session') and request.session:
                request.session.clear()

            store_context_in_session(request, addSnackDataToContext(
                context, 'Invalid client session'))
            return redirect('go_login')
        except Exception:
            traceback.print_exc()
            return go_error(HttpRequest(), {'error': get_app_message('oppo_error'), 'message': get_app_message('oppo_error_message')})
    else:
        return redirect('go_client')


def go_records(request):
    try:
        client = UnoClient.objects.get(client_id=request.session['id'])

        context = {}
        context['entity_name'] = client.entity_name

        customerList = UnoCustomer.objects.filter(client=client)

        if len(customerList) == 0:
            store_context_in_session(
                request, addSnackDataToContext(context, 'No customer found'))
            return redirect('go_client')

        records = {}
        for customer in customerList:
            oppoList = UnoOpportunity.objects.filter(
                client=client, customer=customer)

            if len(oppoList) > 0:
                records[customer.customer_name] = []
                for oppo in oppoList:
                    records[customer.customer_name].append(
                        (oppo.opportunity_number, oppo.creation_time))
            else:
                records[customer.customer_name] = None

        context['records'] = records

        return render(request, 'core/records.html', context=context)
    except Exception:
        traceback.print_exc()
        if request and hasattr(request, 'session'):
            request.session.clear()

        return redirect('go_login')
