"""
View logic used in catalog app
"""

import traceback

from django.db import transaction
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator

from seev.apps.utils.generators import (getFullCatalogCode)
from seev.apps.utils.messages import get_app_message, addSnackDataToContext
from seev.apps.utils.session import store_context_in_session, get_context_in_session
from seev.apps.utils.validations import isValidPrCode

from seev.apps.core.models import UnoClient

from .models import CtgProduct, CtgFeature, CtgSpecification, CtgValue, CtgRestriction, CtgPrice
from .forms import AddPrForm


# Also the add product UI
def go_cat_home(request, context=None):
    try:
        context = get_context_in_session(request)

        if not context:
            context = {}

        ITEMS_PER_PAGE = 3

        productPage = None
        if request.GET.get('pr_page'):
            productPage = request.GET.get('pr_page')
        else:
            productPage = 1

        client = UnoClient.objects.get(client_id=request.session['id'])
        context['client'] = client
        context['addPrForm'] = AddPrForm()

        # Get all products
        prResult = CtgProduct.objects.filter(
            client_id=client.client_id, active=True).order_by('-creation_time', 'itemcode')
        pagedList = Paginator(prResult, ITEMS_PER_PAGE)
        products = pagedList.get_page(productPage)

        for pr in products:
            pr.product_id = str(pr.product_id).replace('-', '')

        context['products'] = products
        context['prCount'] = len(products)

        return render(request, 'catalog/index.html', context=context)
    except Exception:
        traceback.print_exc()
        if request and hasattr(request, 'session'):
            request.session.clear()
        return redirect('go_login')


@transaction.atomic
def add_ctg_pr(request, context=None):
    if request.method == 'POST':
        try:
            prCode = request.POST['product_code']
            prName = request.POST['product_name']

            if not prCode or not prName:
                raise AssertionError

            if not isValidPrCode(prCode) or len(prName) > 128:
                raise AssertionError

            client = UnoClient.objects.get(client_id=request.session['id'])

            # Get namespaced code and check for duplicate
            itemcode = getFullCatalogCode(prCode, client)
            tempPr = CtgProduct.objects.filter(itemcode=itemcode)
            if tempPr and len(tempPr) > 0:
                raise TabError

            newProduct = CtgProduct(
                client=client,
                itemcode=itemcode,
                name=prName
            )

            newProduct.save()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Product added'))
            return redirect('go_cat_home')
        except AssertionError:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Invalid data'))
            return redirect('go_cat_home')
        except TabError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Code already exists'))
            return redirect('go_cat_home')
        except Exception:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')
