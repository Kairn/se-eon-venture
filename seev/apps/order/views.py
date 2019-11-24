"""
View logic used in catalog app
"""

import traceback

from django.db import transaction
from django.shortcuts import render, redirect, reverse

from seev.apps.utils.country import UnoCountry
from seev.apps.utils.generators import (
    getFullCatalogCode, getDefCatalogCode, generateOrderMeta, generateOrderData, getGoogleMapApiSource)
from seev.apps.utils.codetable import getGeneralTranslation
from seev.apps.utils.messages import get_app_message, addSnackDataToContext
from seev.apps.utils.session import *
from seev.apps.utils.process import *

from seev.apps.core.models import UnoClient

from .models import *
from .forms import *


def go_ord_home(request, context=None):
    context = get_context_in_session(request)

    if not context:
        context = {}

    return render(request, 'order/index.html', context=context)


def find_oppo_by_num(request, context=None):
    if request.method == 'POST':
        try:
            oppoNumber = request.POST['opportunity-number']

            opportunity = UnoOpportunity.objects.get(
                opportunity_number=oppoNumber)
            if not opportunity.active or opportunity.deal_count >= opportunity.deal_limit:
                raise AssertionError

            # Get client and customer
            client = UnoClient.objects.get(client_id=opportunity.client_id)
            customer = UnoCustomer.objects.get(
                customer_id=opportunity.customer_id)

            # Fill opportunity details
            oppoData = {}
            opportunity.discount_nrc = getGeneralTranslation(
                opportunity.discount_nrc)
            opportunity.discount_mrc = getGeneralTranslation(
                opportunity.discount_mrc)
            opportunity.opportunity_number = str(
                opportunity.opportunity_number).replace('-', '')
            oppoData['opportunity'] = opportunity
            oppoData['reDeal'] = int(
                opportunity.deal_limit) - int(opportunity.deal_count)
            oppoData['clientName'] = client.entity_name
            oppoData['clientEml'] = client.contact_email
            oppoData['clientPh'] = client.contact_phone
            oppoData['clientCty'] = UnoCountry.get_country_by_code(
                client.country)
            oppoData['custName'] = customer.customer_name
            oppoData['custEml'] = customer.contact_email

            context = {}
            context['oppoData'] = oppoData

            return render(request, 'order/index.html', context=context)
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Opportunity has expired'))
            return redirect('go_ord_home')
        except Exception:
            traceback.print_exc()
            store_context_in_session(request, addSnackDataToContext(
                context, 'Opportunity not found'))
            return redirect('go_ord_home')
    else:
        return redirect('go_ord_home')


@transaction.atomic
def create_order(request, context=None):
    if request.method == 'POST':
        try:
            oppoId = request.POST['opportunity-id']
            ordName = request.POST['order-name']
            ordSecret = request.POST['order-secret']

            # Fetch data
            opportunity = UnoOpportunity.objects.get(opportunity_id=oppoId)
            if not opportunity.active or opportunity.deal_count >= opportunity.deal_limit:
                raise AssertionError
            client = UnoClient.objects.get(client_id=opportunity.client_id)
            customer = UnoCustomer.objects.get(
                customer_id=opportunity.customer_id)

            # Create basket and order
            basket = PtaBasket(
                client=client,
                customer=customer
            )

            order = PtaOrderInstance(
                order_name=ordName,
                secret=ordSecret,
                client=client,
                customer=customer,
                opportunity=opportunity,
                basket=basket,
                status='IN'
            )

            basket.save()
            order.save()

            # Store order in session
            meta = generateOrderMeta(order)
            save_ord_meta_to_session(request, meta)

            return redirect('go_ord_config_home')
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Opportunity invalid or expired'))
            return redirect('go_ord_home')
        except Exception:
            traceback.print_exc()
            store_context_in_session(request, addSnackDataToContext(
                context, 'Order creation failed'))
            return redirect('go_ord_home')
    else:
        return redirect('go_ord_home')


def go_ord_config_home(request, context=None):
    context = get_context_in_session(request)

    if not context:
        context = {}

    # Fill context with order metadata
    context = load_ord_meta_to_context(request, context)
    if not context:
        store_context_in_session(request, addSnackDataToContext(
            context, 'Order request failed'))
        return redirect('go_ord_home')

    order = PtaOrderInstance.objects.get(
        order_number=context['ordMeta']['order_number'])
    context['numSites'] = len(getAllSitesInOrder(order))
    context['numPrs'] = len(getAllProductsInOrder(order))
    context['isValid'] = True if order.status in ('VA', 'FL') else False

    return render(request, 'order/order-home.html', context=context)


def find_ord_by_num(request, context=None):
    if request.method == 'POST':
        try:
            ordNumber = request.POST['order-number']

            order = PtaOrderInstance.objects.get(order_number=ordNumber)

            # Get order data
            ordData = generateOrderData(order)

            context = {}
            context['ordData'] = ordData

            return render(request, 'order/index.html', context=context)
        except Exception:
            traceback.print_exc()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Order not found'))
            return redirect('go_ord_home')
    else:
        return redirect('go_ord_home')


def auth_access_order(request, context=None):
    if request.method == 'POST':
        try:
            ordId = request.POST['order-id']
            ordSec = request.POST['order-secret']

            order = PtaOrderInstance.objects.get(order_instance_id=ordId)

            context = {}
            if ordSec == order.secret:
                meta = generateOrderMeta(order)
                save_ord_meta_to_session(request, meta)

                return redirect('go_ord_config_home')
            else:
                clear_ord_meta(request)
                ordData = generateOrderData(order)
                context['ordData'] = ordData
                context['snack_data'] = 'Invalid secret, access denied'

                return render(request, 'order/index.html', context=context)
        except Exception:
            traceback.print_exc()
            clear_ord_meta(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_ord_home')


def exit_order(request, context=None):
    clear_ord_meta(request)
    return redirect('go_landing')


def go_site_config(request, context=None):
    try:
        context = get_context_in_session(request)

        if not context:
            context = {}

        # Get order metadata
        ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None
        if not ordMeta:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Order request failed'))
            return redirect('go_ord_home')
        else:
            context = load_ord_meta_to_context(request, context)
            context['mapApi'] = getGoogleMapApiSource()

        order = PtaOrderInstance.objects.get(
            order_number=ordMeta['order_number'])

        # Load existing sites
        siteData = []
        sites = getAllSitesInOrder(order)

        for site in sites:
            data = {}
            doc = site.site
            data['id'] = site.pta_site_id
            data['name'] = site.site_name
            data['valid'] = '1' if site.is_valid else '0'
            data['addr'] = ', '.join([doc.address_1, doc.city, doc.country])
            data['state'] = doc.state
            data['prCount'] = len(getAllProductsInSite(site))
            siteData.append(data)

        context['siteData'] = siteData
        context['siteCount'] = len(siteData)

        return render(request, 'order/order-site.html', context=context)
    except Exception:
        traceback.print_exc()
        store_context_in_session(
            request, addSnackDataToContext(context, 'Redirect error'))
        return redirect('go_ord_home')


@transaction.atomic
def add_new_site(request, context=None):
    if request.method == 'POST':
        try:
            context = {}
            ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None

            if not ordMeta:
                return redirect('go_site_config')

            # Get address form data
            siteName = request.POST['site_name']
            addrL1 = request.POST['address_line_1']
            addrL2 = request.POST['address_line_2']
            addrL3 = request.POST['address_line_3']
            city = request.POST['address_city']
            state = request.POST['address_state']
            zipcode = request.POST['address_postal']
            country = request.POST['address_country']

            # Get order
            order = PtaOrderInstance.objects.get(
                order_number=ordMeta['order_number'])
            customer = order.customer

            # Validation
            dupSite = PtaSite.objects.filter(
                order_instance=order, site_name=siteName)
            if len(dupSite) > 0:
                raise TabError

            site = UnoSite.objects.filter(address_1=addrL1, address_2=addrL2, address_3=addrL3,
                                          city=city, state=state, zipcode=zipcode, country=country, customer=customer)
            if len(site) > 0:
                site = site[0]
                extSite = PtaSite.objects.filter(
                    site=site, order_instance=order)
                if len(extSite) > 0:
                    raise AssertionError
            else:
                site = UnoSite(
                    customer=customer,
                    address_1=addrL1,
                    address_2=addrL2,
                    address_3=addrL3,
                    city=city,
                    state=state,
                    zipcode=zipcode,
                    country=country
                )
                site.save()

            ordSite = PtaSite(
                site_name=siteName,
                site=site,
                order_instance=order,
            )

            ordSite.save()
            invalidateOrder(order)
            refreshOrdSessionData(order, request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'New location added'))
            return redirect('go_site_config')
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Site already exists'))
            return redirect('go_site_config')
        except TabError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Location name already exists'))
            return redirect('go_site_config')
        except Exception:
            traceback.print_exc()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_site_config')


@transaction.atomic
def rm_site(request, context=None):
    if request.method == 'POST':
        try:
            context = {}
            ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None

            if not ordMeta:
                return redirect('go_site_config')

            siteId = request.POST['site-id']
            site = PtaSite.objects.get(pta_site_id=siteId)
            order = site.order_instance

            # Delete all products
            products = getAllProductsInSite(site)
            for product in products:
                deleteProductItem(product)

            site.delete()
            invalidateOrder(order)
            refreshOrdSessionData(order, request)
            store_context_in_session(request, addSnackDataToContext(
                context, 'Location has been removed'))
            return redirect('go_site_config')
        except Exception:
            traceback.print_exc()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_site_config')
