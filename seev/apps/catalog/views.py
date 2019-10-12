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
    isValidPrCode, isValidSpecCode, isValidFetCode, isValidBoolean, isValidQuantity)

from seev.apps.core.models import UnoClient

from .models import CtgProduct, CtgFeature, CtgSpecification, CtgValue, CtgRestriction, CtgPrice
from .forms import (AddPrForm, EditPrForm, AddSpecForm,
                    AddFetForm, EditFetForm)


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
            traceback.print_exc()
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
            traceback.print_exc()
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

        context['reUrl'] = reverse('go_cat_home')

        # Load specs
        specs = CtgSpecification.objects.filter(
            parent_ctg_id=product.ctg_doc_id, active=True).order_by('-creation_time', 'leaf_name')
        context['specs'] = specs
        context['spCount'] = len(specs)

        # Load features
        features = CtgFeature.objects.filter(
            client=client, product=product, active=True).order_by('-creation_time', 'itemcode')
        for fet in features:
            fet.itemcode = getDefCatalogCode(fet.itemcode)
        context['features'] = features
        context['fetCount'] = len(features)

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
        context['limit_suffix'] = '(0 for unlimited)'

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
            traceback.print_exc()
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
            if product and len(product) > 0:
                flag = 'PR'
                parentItem = product[0]
            else:
                feature = CtgFeature.objects.filter(
                    client_id=clientId, ctg_doc_id=docId, active=True)
                if feature and len(feature) > 0:
                    flag = 'FET'
                    parentItem = feature[0]
                else:
                    raise AssertionError

            redir = '?doc_id=' + docId
            if flag == 'PR':
                redir = reverse('go_pr_config') + redir
            else:
                redir = reverse('go_fet_config') + redir

            # Validation
            if not leafName or not specName or not dt or not isValidSpecCode(leafName):
                raise ValueError
            if len(leafName) > 32 or len(specName) > 128:
                raise ValueError
            if defVal:
                if (dt == 'BO' and not isValidBoolean(defVal)) or (dt == 'QTY' and not isValidQuantity(defVal)):
                    raise ValueError

            # Set default values
            if dt == 'BO' and not defVal:
                defVal = 0
            elif dt == 'QTY' and not defVal and defVal != 0:
                defVal = 1

            spec = CtgSpecification.objects.filter(
                parent_ctg_id=docId, leaf_name=leafName)
            if spec and len(spec) > 0:
                raise TabError

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
        except TabError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Leaf already exists'))
            return redirect(redir)
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Product/Feature does not exist'))
            return redirect('go_cat_home')
        except Exception:
            traceback.print_exc()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


@transaction.atomic
def add_ctg_fet(request, context=None):
    if request.method == 'POST':
        try:
            productId = request.POST['product_id']
            fetCode = request.POST['feature_code']
            fetName = request.POST['feature_name']
            limit = request.POST['limit']
            extOnly = request.POST['is_extended']

            clientId = request.session['id']

            # Verification
            docId = ''
            pr = None
            product = CtgProduct.objects.filter(
                client_id=clientId, product_id=productId, active=True)
            if not product or len(product) != 1:
                raise AssertionError
            else:
                pr = product[0]
                docId = str(pr.ctg_doc_id).replace('-', '')

            redir = reverse('go_pr_config') + '?doc_id=' + docId

            # Validation
            if not fetCode or not isValidFetCode(fetCode) or not fetName:
                raise ValueError

            fetCode = getFullCatalogCode(fetCode, None, clientId)
            feature = CtgFeature.objects.filter(itemcode=fetCode)
            if (feature and len(feature) > 0):
                raise TabError

            if not limit or not isValidQuantity(limit):
                limit = 0

            newFeature = CtgFeature(
                product=pr,
                client_id=clientId,
                itemcode=fetCode,
                name=fetName,
                limit=limit,
                extended=extOnly
            )

            newFeature.save()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Feature created'))
            return redirect(redir)
        except ValueError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Invalid value encountered'))
            return redirect(redir)
        except TabError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Code already exists'))
            return redirect(redir)
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Product does not exist'))
            return redirect('go_cat_home')
        except Exception:
            traceback.print_exc()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


@transaction.atomic
def rm_ctg_spec(request, context=None):
    if request.method == 'POST':
        try:
            flag = request.POST['flag']
            specId = request.POST['specification_id']

            # Verification
            client = UnoClient.objects.get(client_id=request.session['id'])
            spec = CtgSpecification.objects.get(
                specification_id=specId, active=True)

            redir = '?doc_id=' + str(spec.parent_ctg_id).replace('-', '')
            if flag == 'PR':
                redir = reverse('go_pr_config') + redir
            else:
                redir = reverse('go_fet_config') + redir

            spec.active = False

            spec.save()
            store_context_in_session(request, addSnackDataToContext(
                context, 'Specification removed'))
            return redirect(redir)
        except Exception:
            traceback.print_exc()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


@transaction.atomic
def rm_ctg_fet(request, context=None):
    if request.method == 'POST':
        try:
            fetId = request.POST['feature_id']
            clientId = request.session['id']

            # Verification
            feature = CtgFeature.objects.get(
                client_id=clientId, feature_id=fetId, active=True)
            product = CtgProduct.objects.get(
                product_id=feature.product_id, active=True)

            redir = reverse('go_pr_config') + '?doc_id=' + \
                str(product.ctg_doc_id).replace('-', '')

            feature.active = False

            feature.save()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Feature removed'))
            return redirect(redir)
        except Exception:
            traceback.print_exc()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


def go_fet_config(request, context=None):
    try:
        context = get_context_in_session(request)

        if not context:
            context = {}

        # Get client and feature
        client = UnoClient.objects.get(client_id=request.session['id'])
        feature = CtgFeature.objects.get(ctg_doc_id=request.GET.get(
            'doc_id'), client_id=client.client_id, active=True)

        feature.itemcode = getDefCatalogCode(feature.itemcode)
        context['client'] = client
        context['feature'] = feature

        # Get product URL
        product = CtgProduct.objects.get(product_id=feature.product_id)
        prUrl = reverse('go_pr_config') + '?doc_id=' + \
            str(product.ctg_doc_id).replace('-', '')
        context['reUrl'] = prUrl

        # Load specs
        specs = CtgSpecification.objects.filter(
            parent_ctg_id=feature.ctg_doc_id, active=True).order_by('-creation_time', 'leaf_name')
        context['specs'] = specs
        context['spCount'] = len(specs)

        # Initialize forms
        # Edit feature
        editFetForm = EditFetForm()
        editFetForm.fields['feature_id'].widget.attrs['value'] = str(
            feature.feature_id).replace('-', '')
        editFetForm.fields['feature_code'].widget.attrs['value'] = feature.itemcode
        editFetForm.fields['feature_name'].widget.attrs['value'] = feature.name
        editFetForm.fields['feature_name'].widget.attrs['data-name'] = feature.name
        editFetForm.fields['limit'].widget.attrs['value'] = feature.limit
        editFetForm.fields['limit'].widget.attrs['data-value'] = feature.limit
        editFetForm.fields['is_extended'].widget.attrs['value'] = feature.extended
        editFetForm.fields['is_extended'].widget.attrs['data-value'] = feature.extended
        context['editFetForm'] = editFetForm

        addSpecForm = AddSpecForm()
        addSpecForm.fields['parent_ctg_id'].widget.attrs['value'] = request.GET.get(
            'doc_id')
        context['addSpecForm'] = addSpecForm

        return render(request, 'catalog/feature.html', context=context)
    except Exception:
        traceback.print_exc()
        return redirect('go_cat_home')
