"""
View logic used in catalog app
"""

import traceback

from django.http import HttpRequest, HttpResponse
from django.db import transaction
from django.shortcuts import render, redirect, reverse

from seev.apps.utils.country import UnoCountry
from seev.apps.utils.generators import *
from seev.apps.utils.codetable import getGeneralTranslation
from seev.apps.utils.messages import get_app_message, addSnackDataToContext
from seev.apps.utils.session import *
from seev.apps.utils.process import *

from seev.apps.core.views import go_error, go_success
from seev.apps.core.models import UnoClient

from .models import *


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
        except ObjectDoesNotExist:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Opportunity not found'))
            return redirect('go_ord_home')
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Opportunity has expired'))
            return redirect('go_ord_home')
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown Error'))
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
            # traceback.print_exc()
            logError(request)
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

    # Order validation request
    if 'ord_valid_count' in request.session:
        context['validCnt'] = request.session['ord_valid_count']
        del request.session['ord_valid_count']

    return render(request, 'order/order-home.html', context=context)


def find_ord_by_num(request, context=None):
    if request.method == 'POST':
        try:
            ordNumber = request.POST['order-number']

            # Check order
            order = PtaOrderInstance.objects.get(order_number=ordNumber)
            if order.status not in ('IN', 'IP', 'VA', 'FL'):
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Order cannot be accessed'))
                return redirect('go_ord_home')

            # Get order data
            ordData = generateOrderData(order)

            context = {}
            context['ordData'] = ordData

            return render(request, 'order/index.html', context=context)
        except ObjectDoesNotExist:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Order not found'))
            return redirect('go_ord_home')
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown Error'))
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
            # traceback.print_exc()
            logError(request)
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
        if isOrderLocked(order):
            store_context_in_session(
                request, addSnackDataToContext(context, 'Order is locked'))
            return redirect('go_ord_config_home')

        # Load existing sites
        siteData = []
        sites = getAllSitesInOrder(order)

        for site in sites:
            data = {}
            doc = site.site
            data['id'] = str(site.pta_site_id)
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
        # traceback.print_exc()
        logError(request)
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
            # traceback.print_exc()
            logError(request)
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
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_site_config')


def go_build_pr(request, context=None):
    try:
        context = get_context_in_session(request)

        if not context:
            context = {}

        # Metadata
        ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None
        if not ordMeta:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Order request failed'))
            return redirect('go_ord_home')
        else:
            context = load_ord_meta_to_context(request, context)

        order = PtaOrderInstance.objects.get(
            order_number=ordMeta['order_number'])
        if isOrderLocked(order):
            store_context_in_session(
                request, addSnackDataToContext(context, 'Order is locked'))
            return redirect('go_ord_config_home')

        client = order.client

        # Load catalog products
        ctgList = getAllClientProducts(client)
        ctgData = []
        if not ctgList or len(ctgList) == 0:
            return go_error(HttpRequest(), {'error': get_app_message('catalog_error'), 'message': get_app_message('catalog_error_message')})

        for pr in ctgList:
            prDoc = {}
            prDoc['id'] = str(pr.ctg_doc_id)
            prDoc['code'] = getDefCatalogCode(pr.itemcode)
            prDoc['name'] = pr.name
            ctgData.append(prDoc)
        context['prData'] = ctgData

        # Load Sites
        sites = getAllSitesInOrder(order)
        if len(sites) == 0:
            store_context_in_session(
                request, addSnackDataToContext(context, 'No sites found'))
            return redirect('go_site_config')

        siteData = []
        for site in sites:
            data = {}
            doc = site.site
            data['id'] = str(site.pta_site_id)
            data['name'] = site.site_name
            data['valid'] = '1' if site.is_valid else '0'
            siteData.append(data)
        context['siteData'] = siteData

        # Load current site and products
        site = sites[0]
        siteId = request.GET.get('site_id')
        if siteId:
            sites = sites.filter(pta_site_id=siteId)
            if len(sites) > 0:
                site = sites[0]
            else:
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Requested site not found'))
                return redirect('go_site_config')

        siteDoc = site.site
        context['selId'] = str(site.pta_site_id)
        context['siteDoc'] = siteDoc

        products = getAllProductsInSite(site)
        biData = []
        for bi in products:
            biDoc = {}
            biDoc['id'] = str(bi.basket_item_id)
            biDoc['name'] = getBasketItemName(bi)
            biDoc['serial'] = zeroPrepender(bi.serial, 5)
            biDoc['valid'] = '1' if bi.is_valid else '0'
            biData.append(biDoc)

        context['biData'] = biData
        context['prCount'] = len(biData)

        return render(request, 'order/order-product.html', context=context)
    except Exception:
        # traceback.print_exc()
        logError(request)
        store_context_in_session(
            request, addSnackDataToContext(context, 'Redirect error'))
        return redirect('go_ord_home')


@transaction.atomic
def add_pr_to_basket(request, context=None):
    if request.method == 'POST':
        try:
            context = {}
            ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None

            if not ordMeta:
                return redirect('go_build_pr')

            prData = parseJson(request.POST['ctg_add_data'])
            siteId = request.POST['ord_site_id']

            # Get order details
            order = PtaOrderInstance.objects.get(
                order_number=ordMeta['order_number'])
            site = PtaSite.objects.get(pta_site_id=siteId)
            redir = reverse('go_build_pr') + '?site_id=' + \
                str(site.pta_site_id).replace('-', '')
            leadSerial = getLeadSerialInOrderSite(order, site)
            tempSerial = leadSerial

            if not prData or not leadSerial:
                store_context_in_session(
                    request, addSnackDataToContext(context, 'Invalid order data'))
                return redirect(redir)

            # Add products to basket
            for ctgId, count in prData.items():
                tempSerial = addNewProductsToSite(
                    order, site, ctgId, count, tempSerial)
            invalidateSite(site)
            invalidateOrder(order)
            refreshOrdSessionData(order, request)

            if tempSerial > leadSerial:
                diff = tempSerial - leadSerial
                if diff == 1:
                    store_context_in_session(request, addSnackDataToContext(
                        context, '1 product has been added'))
                else:
                    store_context_in_session(request, addSnackDataToContext(
                        context, str(diff) + ' products have been added'))
            else:
                store_context_in_session(request, addSnackDataToContext(
                    context, 'No product is added'))

            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_build_pr')


@transaction.atomic
def del_pr_in_site(request, context=None):
    if request.method == 'POST':
        try:
            context = {}
            ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None

            if not ordMeta:
                return redirect('go_build_pr')

            biId = request.POST['bi_rm_id']
            siteId = request.POST['ord_site_id']

            site = PtaSite.objects.get(pta_site_id=siteId)
            order = site.order_instance
            item = PtaBasketItem.objects.get(basket_item_id=biId)
            redir = reverse('go_build_pr') + '?site_id=' + \
                str(site.pta_site_id).replace('-', '')

            # Delete process
            deleteProductItem(item)
            invalidateSite(site)
            invalidateOrder(order)
            refreshOrdSessionData(order, request)

            store_context_in_session(request, addSnackDataToContext(
                context, 'Product has been deleted'))
            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_build_pr')


def go_svc_config(request, context=None):
    try:
        context = get_context_in_session(request)

        if not context:
            context = {}

        # Metadata
        ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None
        if not ordMeta:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Order request failed'))
            return redirect('go_ord_home')
        else:
            context = load_ord_meta_to_context(request, context)

        serviceList = []

        order = PtaOrderInstance.objects.get(
            order_number=ordMeta['order_number'])
        if isOrderLocked(order):
            store_context_in_session(
                request, addSnackDataToContext(context, 'Order is locked'))
            return redirect('go_ord_config_home')

        # Get all sites and products
        sites = PtaSite.objects.filter(
            order_instance=order).order_by('site_name')
        if not sites or len(sites) < 1:
            store_context_in_session(
                request, addSnackDataToContext(context, 'No sites found'))
            return redirect('go_ord_config_home')
        else:
            for site in sites:
                products = PtaBasketItem.objects.filter(
                    pta_site=site, parent_id=None).order_by('serial')
                if products and len(products) > 0:
                    for pr in products:
                        serviceList.append(
                            str(pr.basket_item_id).replace('-', ''))

        if len(serviceList) < 1:
            store_context_in_session(
                request, addSnackDataToContext(context, 'No services found'))
            return redirect('go_ord_config_home')

        serviceId = request.GET.get('svc_id') if request.GET.get(
            'svc_id') else serviceList[0]
        if serviceId not in serviceList:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Invalid service'))
            return redirect('go_ord_config_home')

        preSvcId = None
        nxtSvcId = None
        if serviceList.index(serviceId) > 0:
            preSvcId = serviceList[serviceList.index(serviceId) - 1]
        if serviceList.index(serviceId) < len(serviceList) - 1:
            nxtSvcId = serviceList[serviceList.index(serviceId) + 1]
        context['preId'] = preSvcId
        context['nxtId'] = nxtSvcId

        service = PtaBasketItem.objects.get(basket_item_id=serviceId)
        siteDoc = service.pta_site
        addrDoc = siteDoc.site
        svcData = {}
        svcData['id'] = str(service.basket_item_id)
        svcData['name'] = getBasketItemName(service)
        svcData['serial'] = zeroPrepender(service.serial, 5)
        svcData['valid'] = '1' if service.is_valid else '0'

        context['siteDoc'] = siteDoc
        context['addrDoc'] = addrDoc
        context['svcData'] = svcData

        svcBasketDoc = populateServiceDoc(service)

        # Load catalog definitions
        # Product level
        prSpecList = []
        prCtg = CtgProduct.objects.get(ctg_doc_id=service.ctg_doc_id)
        prSpecs = CtgSpecification.objects.filter(
            parent_ctg_id=service.ctg_doc_id, active=1)
        pspCnt = 0
        for psp in prSpecs:
            val = getLeafValueFromSvcDoc(
                svcBasketDoc, service.itemcode, psp.leaf_name)
            if psp.leaf_name == 'SP_BASE':
                prSpecList.insert(0, buildSpecInfo(psp, val))
            else:
                prSpecList.append(buildSpecInfo(psp, val))
                pspCnt += 1

        # Feature level
        prFetList = []
        fetCtg = CtgFeature.objects.filter(
            product=prCtg, active=1).order_by('creation_time')
        fspCnt = 0
        for fet in fetCtg:
            fetDoc = {}
            fetDoc['id'] = str(fet.ctg_doc_id)
            fetDoc['itemcode'] = fet.itemcode
            fetDoc['name'] = fet.name

            fetSpList = []
            fetSpecs = CtgSpecification.objects.filter(
                parent_ctg_id=fet.ctg_doc_id, active=1)
            for fsp in fetSpecs:
                val = getLeafValueFromSvcDoc(
                    svcBasketDoc, fet.itemcode, fsp.leaf_name)
                if fsp.leaf_name == 'SP_BASE':
                    fetSpList.insert(0, buildSpecInfo(fsp, val))
                else:
                    fetSpList.append(buildSpecInfo(fsp, val))
                    fspCnt += 1

            fetDoc['specs'] = fetSpList
            prFetList.append(fetDoc)

        context['prCtgData'] = prSpecList
        context['pspCnt'] = pspCnt
        context['fetCtgData'] = prFetList
        context['fspCnt'] = fspCnt

        # Populate error
        errorList = getOrCreateSvcError(request, str(service.basket_item_id))
        context['errList'] = errorList
        context['errLen'] = len(errorList)

        return render(request, 'order/order-service.html', context=context)
    except Exception:
        # traceback.print_exc()
        logError(request)
        store_context_in_session(
            request, addSnackDataToContext(context, 'Redirect error'))
        return redirect('go_ord_config_home')


@transaction.atomic
def save_svc_config(request, context=None):
    if request.method == 'POST':
        try:
            context = {}
            ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None

            if not ordMeta:
                return redirect('go_svc_config')

            svcDataStruct = parseJson(request.POST['svc_json'])
            svcId = svcDataStruct['svcId']
            pspList = svcDataStruct['pspList']
            fetList = svcDataStruct['fetList']

            # Check order
            order = PtaOrderInstance.objects.get(
                order_number=ordMeta['order_number'])
            basket = order.basket
            productItem = PtaBasketItem.objects.get(basket_item_id=svcId)
            site = productItem.pta_site

            redir = reverse('go_svc_config') + '?svc_id=' + \
                str(svcId).replace('-', '')

            if isOrderLocked(order):
                store_context_in_session(
                    request, addSnackDataToContext(context, 'Order is locked'))
                return redirect('go_ord_config_home')

            # Save product level specs
            saveBaseSpec(productItem)
            for psp in pspList:
                createOrUpdateSpec(psp['id'], productItem, psp['value'])

            # Save features
            for fet in fetList:
                if fet['addFlag']:
                    featureItem = createOrGetFeature(fet['id'], productItem)
                    # Save feature level specs
                    saveBaseSpec(featureItem)
                    for fsp in fet['fspList']:
                        createOrUpdateSpec(
                            fsp['id'], featureItem, fsp['value'])
                else:
                    existFeature = getExistingFeature(productItem, fet['id'])
                    if existFeature:
                        deleteFeatureItem(existFeature)

            clearSitePrice(site)

            # Validation
            valid = True
            errorList = []
            valid = validateProductItem(productItem, errorList)
            saveErrorInMap(request, str(productItem.basket_item_id), errorList)

            if valid:
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Configuration is saved'))
            else:
                invalidateSite(site)
                invalidateOrder(order)
                refreshOrdSessionData(order, request)
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Error(s) detected in service'))
            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_svc_config')


@transaction.atomic
def do_ord_valid(request, context=None):
    if request.method == 'POST':
        try:
            # Metadata
            ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None
            if not ordMeta:
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Order request failed'))
                return redirect('go_ord_home')
            else:
                context = load_ord_meta_to_context(request, context)

            order = PtaOrderInstance.objects.get(
                order_number=ordMeta['order_number'])
            valid = validateOrder(order)
            refreshOrdSessionData(order, request)

            request.session['ord_valid_count'] = valid
            return redirect('go_ord_config_home')
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_ord_config_home')


def go_ord_summary(request, context=None):
    try:
        context = get_context_in_session(request)

        if not context:
            context = {}

        # Metadata
        ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None
        if not ordMeta:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Order request failed'))
            return redirect('go_ord_home')
        else:
            context = load_ord_meta_to_context(request, context)

        order = PtaOrderInstance.objects.get(
            order_number=ordMeta['order_number'])
        if order.status not in ('VA', 'FL'):
            store_context_in_session(request, addSnackDataToContext(
                context, 'Summary is not available'))
            return redirect('go_ord_config_home')

        # Load product/service tree data
        siteDataList = []
        sites = PtaSite.objects.filter(
            order_instance=order).order_by('creation_time')
        if sites and len(sites) > 0:
            for site in sites:
                populateSiteSummary(siteDataList, site)
        context['siteDataList'] = siteDataList

        return render(request, 'order/order-summary.html', context=context)
    except Exception:
        # traceback.print_exc()
        logError(request)
        store_context_in_session(
            request, addSnackDataToContext(context, 'Unknown error'))
        return redirect('go_ord_config_home')


@transaction.atomic
def do_site_price(request, context=None):
    if request.method == 'POST':
        try:
            ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None

            if not ordMeta:
                return redirect('go_ord_summary')

            siteIds = request.POST['site_array']
            siteList = str(siteIds).split(',') if siteIds else None
            sites = []

            # Check sites
            order = PtaOrderInstance.objects.get(
                order_number=ordMeta['order_number'])
            if siteList and len(siteList) > 0:
                for sid in siteList:
                    site = PtaSite.objects.get(pta_site_id=sid)
                    if site.order_instance.order_instance_id == order.order_instance_id:
                        sites.append(site)

            if sites and len(sites) > 0:
                for site in sites:
                    # Do pricing
                    priceSite(site)
            else:
                store_context_in_session(
                    request, addSnackDataToContext(context, 'No site to price'))
                return redirect('go_ord_summary')

            store_context_in_session(request, addSnackDataToContext(
                context, 'Pricing is received'))
            return redirect('go_ord_summary')
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_ord_summary')


@transaction.atomic
def do_ord_submit(request, context=None):
    if request.method == 'POST':
        try:
            ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None

            if not ordMeta:
                return redirect('go_ord_summary')

            order = PtaOrderInstance.objects.get(
                order_number=ordMeta['order_number'])

            # Validation
            if order.status == 'VA':
                order.status = 'FL'
                basket = order.basket
                basket.is_locked = True

                # Send external request here
                # No code is provided due to the nature of this project

                # Archive record
                oldAr = UnoOrder.objects.filter(
                    order_number=order.order_number)
                if not oldAr or len(oldAr) < 1:
                    arOrder = UnoOrder(
                        order_number=order.order_number,
                        client=order.client,
                        customer=order.customer,
                        opportunity=order.opportunity,
                        status='SM'
                    )
                    arOrder.save()

                    # Increase deal count
                    oppo = order.opportunity
                    oppo.deal_count += 1
                    oppo.save()

                basket.save()
                order.save()
                clear_ord_meta(request)

                return go_success(HttpRequest(), {'message': get_app_message('order_submit_message')})
            else:
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Cannot submit this order'))
                return redirect('go_ord_config_home')
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_ord_summary')


@transaction.atomic
def do_ord_cancel(request, context=None):
    if request.method == 'POST':
        try:
            ordMeta = request.session['order_meta'] if 'order_meta' in request.session else None

            if not ordMeta:
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Order request failed'))
                return redirect('go_ord_home')

            order = PtaOrderInstance.objects.get(
                order_number=ordMeta['order_number'])

            if order.status in ('IN', 'IP', 'VA'):
                order.status = 'VD'
                basket = order.basket
                basket.is_locked = True

                basket.save()
                order.save()
                clear_ord_meta(request)

                return go_success(HttpRequest(), {'message': get_app_message('order_cancel_message')})
            else:
                store_context_in_session(request, addSnackDataToContext(
                    context, 'Invalid cancellation request'))
                return redirect('go_ord_config_home')
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unknown error'))
            return redirect('go_ord_config_home')
    else:
        return redirect('go_ord_config_home')
