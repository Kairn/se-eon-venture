"""
View logic used in catalog app
"""

import traceback

from django.db import transaction
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator

from seev.apps.utils.process import (
    removeProductCascade, removeFeatureCascade, removeSpecCascade, logError)
from seev.apps.utils.generators import (getFullCatalogCode, getDefCatalogCode)
from seev.apps.utils.codetable import getGeneralTranslation
from seev.apps.utils.messages import get_app_message, addSnackDataToContext
from seev.apps.utils.session import store_context_in_session, get_context_in_session
from seev.apps.utils.validations import (
    isValidPrCode, isValidSpecCode, isValidFetCode, isValidBoolean, isValidQuantity)

from seev.apps.core.models import UnoClient

from .models import CtgProduct, CtgFeature, CtgSpecification, CtgValue, CtgRestriction, CtgPrice
from .forms import (AddPrForm, EditPrForm, AddSpecForm, AddFetForm,
                    EditFetForm, EditSpecForm, AddValueForm, RestrictionForm, PriceForm)


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
        # traceback.print_exc()
        logError(request)
        if request and hasattr(request, 'session'):
            request.session.clear()

        store_context_in_session(
            request, addSnackDataToContext(context, 'Unknown Error'))
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
            # traceback.print_exc()
            logError(request)
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
            # Cascade process
            removeProductCascade(product)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Product removed'))
            return redirect('go_cat_home')
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Product does not exist'))
            return redirect('go_cat_home')
        except Exception:
            # traceback.print_exc()
            logError(request)
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
        # traceback.print_exc()
        logError(request)
        store_context_in_session(
            request, addSnackDataToContext(context, 'Unknown Error'))
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
            # traceback.print_exc()
            logError(request)
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
            # traceback.print_exc()
            logError(request)
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
            # traceback.print_exc()
            logError(request)
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
            # Cascade process
            removeSpecCascade(spec.specification_id)
            store_context_in_session(request, addSnackDataToContext(
                context, 'Specification removed'))
            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
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
            # Cascade process
            removeFeatureCascade(feature.ctg_doc_id)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Feature removed'))
            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
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
        context['pntText'] = getDefCatalogCode(product.itemcode)

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
        # traceback.print_exc()
        logError(request)
        store_context_in_session(
            request, addSnackDataToContext(context, 'Unknown Error'))
        return redirect('go_cat_home')


@transaction.atomic
def chg_fet(request, context=None):
    if request.method == 'POST':
        try:
            featureId = request.POST['feature_id']
            newFetName = request.POST['feature_name']
            newLimit = request.POST['limit']
            newExt = request.POST['is_extended']

            # Verification
            clientId = request.session['id']
            feature = CtgFeature.objects.filter(
                client_id=clientId, feature_id=featureId, active=True)
            if not feature or len(feature) < 1:
                raise AssertionError

            feature = feature[0]
            docId = str(feature.ctg_doc_id).replace('-', '')
            redir = reverse('go_fet_config') + '?doc_id=' + docId

            feature.name = newFetName
            if newLimit and isValidQuantity(newLimit):
                feature.limit = newLimit
            feature.extended = newExt

            feature.save()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Feature updated'))
            return redirect(redir)
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Feature does not exist'))
            return redirect('go_cat_home')
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


def go_spec_config(request, context=None):
    try:
        context = get_context_in_session(request)

        if not context:
            context = {}

        # Load specification
        client = UnoClient.objects.get(client_id=request.session['id'])
        specification = CtgSpecification.objects.get(
            ctg_doc_id=request.GET.get('doc_id'), active=True)

        context['client'] = client
        context['specification'] = specification

        # Get parent URL
        flag = ''
        pntUrl = ''
        pntText = ''
        product = CtgProduct.objects.filter(
            ctg_doc_id=specification.parent_ctg_id, client=client, active=True)
        if product and len(product) > 0:
            flag = 'PR'
            pntText = getDefCatalogCode(product[0].itemcode)
            pntUrl = reverse('go_pr_config') + '?doc_id=' + \
                str(product[0].ctg_doc_id).replace('-', '')
        else:
            feature = CtgFeature.objects.filter(
                ctg_doc_id=specification.parent_ctg_id, client=client, active=True)
            if feature and len(feature) > 0:
                flag = 'FET'
                pntText = getDefCatalogCode(feature[0].itemcode)
                pntUrl = reverse('go_fet_config') + '?doc_id=' + \
                    str(feature[0].ctg_doc_id).replace('-', '')

        if not flag:
            raise Exception
        context['reUrl'] = pntUrl
        context['pntText'] = pntText

        # Spec config details
        # Values
        values = CtgValue.objects.filter(
            specification=specification).order_by('-creation_time', 'code')
        context['values'] = values
        context['valCount'] = len(values)

        # Spec edit form
        editSpecForm = EditSpecForm()
        editSpecForm.fields['specification_id'].widget.attrs['value'] = str(
            specification.specification_id).replace('-', '')
        editSpecForm.fields['leaf_name'].widget.attrs['value'] = specification.leaf_name
        editSpecForm.fields['data_type'].widget.attrs['value'] = getGeneralTranslation(
            specification.data_type)
        editSpecForm.fields['spec_label'].widget.attrs['value'] = specification.label
        editSpecForm.fields['spec_label'].widget.attrs['data-name'] = specification.label
        editSpecForm.fields['default_value'].widget.attrs['value'] = specification.default_value
        editSpecForm.fields['default_value'].widget.attrs['data-value'] = specification.default_value
        context['editSpecForm'] = editSpecForm

        dt = specification.data_type

        # Other config forms
        # Value form
        if dt == 'ENUM':
            addValueForm = AddValueForm()
            addValueForm.fields['specification_id'].widget.attrs['value'] = str(
                specification.specification_id).replace('-', '')
            context['addValueForm'] = addValueForm

        # Restriction form
        if dt == 'STR' or dt == 'QTY':
            resForm = RestrictionForm()
            resForm.fields['specification_id'].widget.attrs['value'] = str(
                specification.specification_id).replace('-', '')
            # Retrieve and populate
            resList = CtgRestriction.objects.filter(
                specification=specification)
            for res in resList:
                if res.rule_type == 'MAX':
                    resForm.fields['max_val'].widget.attrs['value'] = res.value
                    resForm.fields['max_val'].widget.attrs['data-value'] = res.value
                elif res.rule_type == 'MIN':
                    resForm.fields['min_val'].widget.attrs['value'] = res.value
                    resForm.fields['min_val'].widget.attrs['data-value'] = res.value
                elif res.rule_type == 'UPLEN':
                    resForm.fields['max_len'].widget.attrs['value'] = res.value
                    resForm.fields['max_len'].widget.attrs['data-value'] = res.value
                elif res.rule_type == 'LOLEN':
                    resForm.fields['min_len'].widget.attrs['value'] = res.value
                    resForm.fields['min_len'].widget.attrs['data-value'] = res.value
                elif res.rule_type == 'AO':
                    resForm.fields['alpha_only'].widget.attrs['value'] = res.value
                    resForm.fields['alpha_only'].widget.attrs['data-value'] = res.value
                elif res.rule_type == 'NUO':
                    resForm.fields['num_only'].widget.attrs['value'] = res.value
                    resForm.fields['num_only'].widget.attrs['data-value'] = res.value
                elif res.rule_type == 'EML':
                    resForm.fields['email_only'].widget.attrs['value'] = res.value
                    resForm.fields['email_only'].widget.attrs['data-value'] = res.value
                elif res.rule_type == 'NN':
                    resForm.fields['not_null'].widget.attrs['value'] = res.value
                    resForm.fields['not_null'].widget.attrs['data-value'] = res.value
            # Disable not applicable rules
            if dt == 'STR':
                resForm.fields['max_val'].widget.attrs['disabled'] = 'true'
                resForm.fields['max_val'].widget.attrs['class'] = 'form-inp-dis'
                resForm.fields['min_val'].widget.attrs['disabled'] = 'true'
                resForm.fields['min_val'].widget.attrs['class'] = 'form-inp-dis'
            elif dt == 'QTY':
                resForm.fields['max_len'].widget.attrs['disabled'] = 'true'
                resForm.fields['max_len'].widget.attrs['class'] = 'form-inp-dis'
                resForm.fields['min_len'].widget.attrs['disabled'] = 'true'
                resForm.fields['min_len'].widget.attrs['class'] = 'form-inp-dis'
                resForm.fields['alpha_only'].widget.attrs['disabled'] = 'true'
                resForm.fields['alpha_only'].widget.attrs['class'] = 'form-inp-dis'
                resForm.fields['num_only'].widget.attrs['disabled'] = 'true'
                resForm.fields['num_only'].widget.attrs['class'] = 'form-inp-dis'
                resForm.fields['email_only'].widget.attrs['disabled'] = 'true'
                resForm.fields['email_only'].widget.attrs['class'] = 'form-inp-dis'
            context['resForm'] = resForm

        # Price form
        priceForm = PriceForm()
        priceForm.fields['specification_id'].widget.attrs['value'] = str(
            specification.specification_id).replace('-', '')
        # Retrieve data
        priceList = CtgPrice.objects.filter(
            specification=specification).order_by('creation_time')
        # Populate price point(s)
        priceData = {}
        for price in priceList:
            data = (price.mrc, price.nrc, price.unit_mrc, price.unit_nrc)
            if not price.value:
                priceData['$'] = data
            else:
                priceData[price.value.code] = data
        context['priceData'] = priceData if len(priceData) > 0 else None
        # Disable fields
        priceForm.fields['value'].widget.attrs['disabled'] = 'true'
        priceForm.fields['value'].widget.attrs['class'] = 'form-inp-dis'
        if dt == 'QTY':
            priceForm.fields['mrc'].widget.attrs['disabled'] = 'true'
            priceForm.fields['mrc'].widget.attrs['class'] = 'form-inp-dis'
            priceForm.fields['nrc'].widget.attrs['disabled'] = 'true'
            priceForm.fields['nrc'].widget.attrs['class'] = 'form-inp-dis'
        else:
            priceForm.fields['unit_mrc'].widget.attrs['disabled'] = 'true'
            priceForm.fields['unit_mrc'].widget.attrs['class'] = 'form-inp-dis'
            priceForm.fields['unit_nrc'].widget.attrs['disabled'] = 'true'
            priceForm.fields['unit_nrc'].widget.attrs['class'] = 'form-inp-dis'
        if dt == 'ENUM' and len(values) > 0:
            # Populate values
            valueList = []
            for val in values:
                valueList.append((val.code, val.translation))
            priceForm.fields['value'].choices = valueList
            priceForm.fields['value'].widget.attrs.pop('disabled', None)
            priceForm.fields['value'].widget.attrs.pop('class', None)
        context['priceForm'] = priceForm

        return render(request, 'catalog/specification.html', context=context)
    except Exception:
        # traceback.print_exc()
        logError(request)
        store_context_in_session(
            request, addSnackDataToContext(context, 'Unknown Error'))
        return redirect('go_cat_home')


@transaction.atomic
def chg_spec(request, context=None):
    if request.method == 'POST':
        try:
            specificationId = request.POST['specification_id']
            newLabel = request.POST['spec_label']
            newDv = request.POST['default_value']

            # Verification
            client = UnoClient.objects.get(client_id=request.session['id'])
            specification = CtgSpecification.objects.get(
                specification_id=specificationId, active=True)
            dt = specification.data_type

            redir = reverse('go_spec_config') + '?doc_id=' + \
                str(specification.ctg_doc_id).replace('-', '')

            # Validation
            if newLabel and len(newLabel) <= 128:
                specification.label = newLabel
            if newDv:
                if (dt == 'BO' and isValidBoolean(newDv)) or (dt == 'QTY' and isValidQuantity(newDv)):
                    specification.default_value = newDv
                elif dt == 'STR' or dt == 'ENUM':
                    specification.default_value = newDv

            specification.save()
            store_context_in_session(request, addSnackDataToContext(
                context, 'Specification updated'))
            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


@transaction.atomic
def add_ctg_val(request, context=None):
    if request.method == 'POST':
        try:
            specificationId = request.POST['specification_id']
            code = request.POST['code']
            translation = request.POST['translation']

            # Verification
            client = UnoClient.objects.get(client_id=request.session['id'])
            specification = CtgSpecification.objects.get(
                specification_id=specificationId, active=True)

            redir = reverse('go_spec_config') + '?doc_id=' + \
                str(specification.ctg_doc_id).replace('-', '')

            # Validation
            if not code or not transaction:
                raise AssertionError
            value = CtgValue.objects.filter(
                specification=specification, code=code)
            if value and len(value) > 0:
                raise TabError

            newValue = CtgValue(
                specification=specification,
                code=code,
                translation=translation
            )

            newValue.save()
            store_context_in_session(request, addSnackDataToContext(
                context, 'Enumeration created'))
            return redirect(redir)
        except AssertionError:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Invalid data'))
            return redirect(redir)
        except TabError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Code already exists'))
            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


@transaction.atomic
def save_ctg_res(request, context=None):
    if request.method == 'POST':
        try:
            specificationId = request.POST['specification_id']
            maxVal = request.POST['max_val'] if 'max_val' in request.POST else None
            minVal = request.POST['min_val'] if 'min_val' in request.POST else None
            maxLen = request.POST['max_len'] if 'max_len' in request.POST else None
            minLen = request.POST['min_len'] if 'min_len' in request.POST else None
            alo = request.POST['alpha_only'] if 'alpha_only' in request.POST else 'N'
            numo = request.POST['num_only'] if 'num_only' in request.POST else 'N'
            emlo = request.POST['email_only'] if 'email_only' in request.POST else 'N'
            nn = request.POST['not_null']

            # Verification
            client = UnoClient.objects.get(client_id=request.session['id'])
            specification = CtgSpecification.objects.get(
                specification_id=specificationId, active=True)

            redir = reverse('go_spec_config') + '?doc_id=' + \
                str(specification.ctg_doc_id).replace('-', '')

            dt = specification.data_type
            if dt != 'STR' and dt != 'QTY':
                raise Exception

            # Get restriction data
            rMav = None
            rMiv = None
            rMal = None
            rMiL = None
            rAo = None
            rNo = None
            rEo = None
            rNn = None
            resList = CtgRestriction.objects.filter(
                specification_id=specificationId)
            for res in resList:
                if res.rule_type == 'MAX':
                    rMav = res
                elif res.rule_type == 'MIN':
                    rMiv = res
                elif res.rule_type == 'UPLEN':
                    rMal = res
                elif res.rule_type == 'LOLEN':
                    rMiL = res
                elif res.rule_type == 'AO':
                    rAo = res
                elif res.rule_type == 'NUO':
                    rNo = res
                elif res.rule_type == 'EML':
                    rEo = res
                elif res.rule_type == 'NN':
                    rNn = res

            if dt == 'STR':
                if maxLen and minLen and int(maxLen) < int(minLen):
                    raise AssertionError
                if alo == 'Y' and (numo == 'Y' or emlo == 'Y'):
                    raise AssertionError
                elif numo == 'Y' and (alo == 'Y' or emlo == 'Y'):
                    raise AssertionError
                elif emlo == 'Y' and (alo == 'Y' or numo == 'Y'):
                    raise AssertionError

                if maxLen and isValidQuantity(maxLen) and maxLen != '0':
                    if rMal and rMal.value != maxLen:
                        rMal.value = maxLen
                        rMal.save()
                    elif not rMal:
                        uplenRule = CtgRestriction(
                            specification=specification,
                            rule_type='UPLEN',
                            value=maxLen
                        )
                        uplenRule.save()
                elif not maxLen and rMal:
                    rMal.delete()
                if minLen and isValidQuantity(minLen) and minLen != '0':
                    if rMiL and rMiL.value != minLen:
                        rMiL.value = minLen
                        rMiL.save()
                    elif not rMiL:
                        lolenRule = CtgRestriction(
                            specification=specification,
                            rule_type='LOLEN',
                            value=minLen
                        )
                        lolenRule.save()
                elif not minLen and rMiL:
                    rMiL.delete()

                if rAo and rAo.value != alo:
                    rAo.value = alo
                    rAo.save()
                elif not rAo and alo == 'Y':
                    aoRule = CtgRestriction(
                        specification=specification,
                        rule_type='AO',
                        value=alo
                    )
                    aoRule.save()
                if rNo and rNo.value != numo:
                    rNo.value = numo
                    rNo.save()
                elif not rNo and numo == 'Y':
                    nuoRule = CtgRestriction(
                        specification=specification,
                        rule_type='NUO',
                        value=numo
                    )
                    nuoRule.save()
                if rEo and rEo.value != emlo:
                    rEo.value = emlo
                    rEo.save()
                elif not rEo and emlo == 'Y':
                    emlRule = CtgRestriction(
                        specification=specification,
                        rule_type='EML',
                        value=emlo
                    )
                    emlRule.save()

            if dt == 'QTY':
                if maxVal and minVal and int(maxVal) < int(minVal):
                    raise AssertionError

                if maxVal and isValidQuantity(maxVal) and maxVal != '0':
                    if rMav and rMav.value != maxVal:
                        rMav.value = maxVal
                        rMav.save()
                    elif not rMav:
                        maxRule = CtgRestriction(
                            specification=specification,
                            rule_type='MAX',
                            value=maxVal
                        )
                        maxRule.save()
                elif not maxVal and rMav:
                    rMav.delete()
                if minVal and isValidQuantity(minVal) and minVal != '0':
                    if rMiv and rMiv.value != minVal:
                        rMiv.value = minVal
                        rMiv.save()
                    elif not rMiv:
                        minRule = CtgRestriction(
                            specification=specification,
                            rule_type='MIN',
                            value=minVal
                        )
                        minRule.save()
                elif not minVal and rMiv:
                    rMiv.delete()

            if rNn:
                if rNn.value != nn:
                    rNn.value = nn
                    rNn.save()
            elif nn == 'Y':
                nnRule = CtgRestriction(
                    specification=specification,
                    rule_type='NN',
                    value=nn
                )
                nnRule.save()

            store_context_in_session(request, addSnackDataToContext(
                context, 'Restrictions updated'))
            return redirect(redir)
        except ValueError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Invalid value encountered'))
            return redirect(redir)
        except AssertionError:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Rule conflict'))
            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


@transaction.atomic
def save_ctg_price(request, context=None):
    if request.method == 'POST':
        try:
            specificationId = request.POST['specification_id']
            mrc = request.POST['mrc'] if 'mrc' in request.POST else None
            nrc = request.POST['nrc'] if 'nrc' in request.POST else None
            uMrc = request.POST['unit_mrc'] if 'unit_mrc' in request.POST else None
            uNrc = request.POST['unit_nrc'] if 'unit_nrc' in request.POST else None
            value = request.POST['value'] if 'value' in request.POST else None

            # Verification
            client = UnoClient.objects.get(client_id=request.session['id'])
            specification = CtgSpecification.objects.get(
                specification_id=specificationId, active=True)
            if value:
                value = CtgValue.objects.get(
                    specification=specification, code=value)

            redir = reverse('go_spec_config') + '?doc_id=' + \
                str(specification.ctg_doc_id).replace('-', '')

            dt = specification.data_type

            # Validation
            try:
                mrc = round(float(mrc), 2) if mrc else None
                nrc = round(float(nrc), 2) if nrc else None
                uMrc = round(float(uMrc), 2) if uMrc else None
                uNrc = round(float(uNrc), 2) if uNrc else None
            except Exception:
                raise AssertionError

            if (mrc and mrc <= 0) or (nrc and nrc <= 0) or (uMrc and uMrc <= 0) or (uNrc and uNrc <= 0):
                raise AssertionError

            # Retrieve price
            price = CtgPrice.objects.filter(
                specification=specification, value=value)
            if len(price) > 0:
                price = price[0]
                price.mrc = mrc
                price.nrc = nrc
                price.unit_mrc = uMrc
                price.unit_nrc = uNrc
            else:
                price = CtgPrice(
                    specification=specification,
                    mrc=mrc,
                    nrc=nrc,
                    unit_mrc=uMrc,
                    unit_nrc=uNrc,
                    value=value
                )

            price.save()
            store_context_in_session(
                request, addSnackDataToContext(context, 'Price point saved'))
            return redirect(redir)
        except AssertionError:
            store_context_in_session(
                request, addSnackDataToContext(context, 'Invalid data'))
            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')


@transaction.atomic
def rm_ctg_val(request, context=None):
    if request.method == 'POST':
        try:
            valueId = request.POST['value_id']

            # Verification
            client = UnoClient.objects.get(client_id=request.session['id'])
            value = CtgValue.objects.get(value_id=valueId)
            spec = CtgSpecification.objects.get(
                specification_id=value.specification_id, active=True)

            redir = reverse('go_spec_config') + '?doc_id=' + \
                str(spec.ctg_doc_id).replace('-', '')

            value.delete()

            store_context_in_session(request, addSnackDataToContext(
                context, 'Enumeration removed'))
            return redirect(redir)
        except Exception:
            # traceback.print_exc()
            logError(request)
            store_context_in_session(
                request, addSnackDataToContext(context, 'Unexpected error'))
            return redirect('go_cat_home')
    else:
        return redirect('go_cat_home')
