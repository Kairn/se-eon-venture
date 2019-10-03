"""
View logic used in catalog app
"""

import traceback

from django.db import transaction
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator

from seev.apps.utils.generators import (getFullCatalogCode, getDefCatalogCode)
from seev.apps.utils.messages import get_app_message, addSnackDataToContext
from seev.apps.utils.session import store_context_in_session, get_context_in_session
from seev.apps.utils.validations import (
    isValidPrCode, isValidSpecCode, isValidBoolean, isValidQuantity)

from seev.apps.core.models import UnoClient

from .models import CtgProduct, CtgFeature, CtgSpecification, CtgValue, CtgRestriction, CtgPrice
from .forms import (AddPrForm, EditPrForm, AddSpecForm, AddFetForm)


# Also the add product UI
def go_cat_home(request, context=None):
    try:
        context = get_context_in_session(request)

        if not context:
            context = {}

        ITEMS_PER_PAGE = 10

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
            pr.itemcode = getDefCatalogCode(pr.itemcode)

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
                request, addSnackDataToContext(context, 'Product created'))
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


@transaction.atomic
def rm_ctg_pr(request, context=None):
    if request.method == 'POST':
        try:
            productId = request.POST['product_id']

            # Client session verification
            client = UnoClient.objects.get(client_id=request.session['id'])

            # Product verification
            product = CtgProduct.objects.filter(
                client_id=client.client_id, product_id=productId, active=True)
            if not product or len(product) < 1:
                raise AssertionError

            product = product[0]
            product.active = False

            product.save()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Product removed'))
            return redirect('go_cat_home')
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Product does not exist'))
            return redirect('go_cat_home')
        except Exception:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


def go_pr_config(request, context=None):
    try:
        context = get_context_in_session(request)

        if not context:
            context = {}

        # Get client and product
        client = UnoClient.objects.get(client_id=request.session['id'])
        product = CtgProduct.objects.get(
            ctg_doc_id=request.GET.get('doc_id'), client_id=client.client_id, active=True)

        product.itemcode = getDefCatalogCode(product.itemcode)
        context['client'] = client
        context['product'] = product

        # Load features
        # Load specs

        # Initialize forms
        editPrForm = EditPrForm()
        editPrForm.fields['product_id'].widget.attrs['value'] = str(
            product.product_id).replace('-', '')
        editPrForm.fields['product_code'].widget.attrs['value'] = product.itemcode
        editPrForm.fields['product_name'].widget.attrs['value'] = product.name
        editPrForm.fields['product_name'].widget.attrs['data-name'] = product.name
        context['editPrForm'] = editPrForm

        addSpecForm = AddSpecForm()
        addSpecForm.fields['parent_ctg_id'].widget.attrs['value'] = request.GET.get(
            'doc_id')
        context['addSpecForm'] = addSpecForm

        addFetForm = AddFetForm()
        addFetForm.fields['product_id'].widget.attrs['value'] = str(
            product.product_id).replace('-', '')
        context['addFetForm'] = addFetForm

        return render(request, 'catalog/product.html', context=context)
    except Exception:
        traceback.print_exc()
        return redirect('go_cat_home')


@transaction.atomic
def chg_pr_name(request, context=None):
    if request.method == 'POST':
        try:
            productId = request.POST['product_id']
            newPrName = request.POST['product_name']

            # Verification
            clientId = request.session['id']
            product = CtgProduct.objects.filter(
                client_id=clientId, product_id=productId, active=True)
            if not product or len(product) < 1:
                raise AssertionError

            product = product[0]
            product.name = newPrName
            docId = str(product.ctg_doc_id).replace('-', '')
            redir = reverse('go_pr_config') + '?doc_id=' + docId

            product.save()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Product updated'))
            return redirect(redir)
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Product does not exist'))
            return redirect('go_cat_home')
        except Exception:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


@transaction.atomic
def add_ctg_spec(request, context=None):
    if request.method == 'POST':
        try:
            docId = request.POST['parent_ctg_id']
            leafName = request.POST['leaf_name']
            specName = request.POST['spec_label']
            dt = request.POST['data_type']
            defVal = request.POST['default_value']

            clientId = request.session['id']

            # Verification
            flag = ''
            parentItem = None
            product = CtgProduct.objects.filter(
                client_id=clientId, ctg_doc_id=docId, active=True)
            if (product and len(product) > 0):
                flag = 'PR'
                parentItem = product[0]
            else:
                feature = CtgFeature.objects.filter(
                    client_id=clientId, ctg_doc_id=docId, active=True)
                if (feature and len(feature) > 0):
                    flag = 'FET'
                    parentItem = feature[0]
                else:
                    raise AssertionError

            redir = '?doc_id=' + docId
            if (flag == 'PR'):
                redir = reverse('go_pr_config') + redir
            else:
                redir = reverse('go_fet_config') + redir

            # Validation
            if (not leafName or not specName or not dt or not isValidSpecCode(leafName)):
                raise ValueError
            if (len(leafName) > 32 or len(specName) > 128):
                raise ValueError
            if (defVal):
                if (dt == 'BO' and not isValidBoolean(defVal)) or (dt == 'QTY' and not isValidQuantity(defVal)):
                    raise ValueError

            newSpec = CtgSpecification(
                parent_ctg_id=docId,
                leaf_name=leafName,
                label=specName,
                data_type=dt,
                default_value=defVal
            )

            newSpec.save()
            store_context_in_session(request, addSnackDataToContext(
                context, 'Specification created'))
            return redirect(redir)
        except ValueError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Invalid value encountered'))
            return redirect(redir)
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Product/Feature does not exist'))
            return redirect('go_cat_home')
        except Exception:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')
