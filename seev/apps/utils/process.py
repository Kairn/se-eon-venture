"""
Handle background tasks used by view logic
"""

import traceback
from django.db import transaction

from seev.apps.core.models import *
from seev.apps.catalog.models import *
from seev.apps.order.models import *

from seev.apps.utils.generators import *
from seev.apps.utils.session import *
from seev.apps.utils.validations import *


@transaction.atomic
def removeProductCascade(product):
    features = CtgFeature.objects.filter(product=product)
    specifications = CtgSpecification.objects.filter(
        parent_ctg_id=product.ctg_doc_id)

    # Disable product specs
    for spec in specifications:
        if not spec.active:
            continue
        spec.active = False
        spec.save()
        removeSpecCascade(spec.specification_id)

    # Disable features
    for fet in features:
        if not fet.active:
            continue
        # Disable feature
        fet.active = False
        fet.save()
        removeFeatureCascade(fet.ctg_doc_id)


@transaction.atomic
def removeFeatureCascade(fetDocId):
    specifications = CtgSpecification.objects.filter(parent_ctg_id=fetDocId)

    for spec in specifications:
        if not spec.active:
            continue
        # Disable spec
        spec.active = False
        spec.save()
        # Cascade
        removeSpecCascade(spec.specification_id)


@transaction.atomic
def removeSpecCascade(specificationId):
    # Remove values
    values = CtgValue.objects.filter(specification_id=specificationId)
    values.delete()

    # Remove restrictions
    restrictions = CtgRestriction.objects.filter(
        specification_id=specificationId)
    restrictions.delete()

    # Remove price points
    prices = CtgPrice.objects.filter(specification_id=specificationId)
    prices.delete()


def getAllClientProducts(client):
    if not client:
        return

    return CtgProduct.objects.filter(client=client, active=True).order_by('name')


def getAllSitesInOrder(order):
    if not order:
        return None

    return PtaSite.objects.filter(order_instance=order).order_by('creation_time')


def getAllProductsInOrder(order):
    if not order:
        return None

    return PtaBasketItem.objects.filter(basket=order.basket, parent_id=None)


def getAllProductsInSite(site):
    if not site:
        return None

    return PtaBasketItem.objects.filter(pta_site=site, parent_id=None).order_by('creation_time')


@transaction.atomic
def startOrder(order):
    if not order:
        return

    if order.status == 'IP':
        return
    elif order.status in ('IN', 'FZ'):
        # Unlock basket
        if order.status == 'FZ':
            basket = order.basket
            if basket:
                basket.is_locked = False
                basket.save()

        order.status = 'IP'
        order.save()


@transaction.atomic
def freezeOrder(order):
    if not order:
        return

    if order.status == 'FZ':
        return
    elif order.status in ('IN', 'IP', 'VA'):
        order.status = 'FZ'
        order.save()

        # Lock basket
        basket = order.basket
        if basket:
            basket.is_locked = True
            basket.save()


@transaction.atomic
def invalidateOrder(order):
    if not order:
        return

    if order.status in ('IN', 'IP', 'VA'):
        order.status = 'IP'
        order.save()


def isOrderLocked(order):
    if not order:
        return False

    if order.status in ('FL', 'FZ', 'EX', 'VD'):
        return True
    elif order.basket.is_locked:
        return True

    return False


@transaction.atomic
def deleteFeatureItem(item):
    if item and item.parent_id:
        item.delete()


@transaction.atomic
def deleteProductItem(item):
    if not item or item.parent_id:
        return

    # Delete child features
    features = PtaBasketItem.objects.filter(parent_id=item.basket_item_id)
    for fet in features:
        fet.delete()

    item.delete()


@transaction.atomic
def addNewProductsToSite(order, site, ctgId, count, beginSerial):
    if not order or not site or not ctgId or not count or not beginSerial:
        return 0

    tempSerial = beginSerial

    try:
        ctgItem = CtgProduct.objects.get(
            ctg_doc_id=ctgId, client=order.client, active=True)

        for i in range(count):
            prItem = PtaBasketItem(
                parent_id=None,
                basket=order.basket,
                ctg_doc_id=ctgItem.ctg_doc_id,
                itemcode=ctgItem.itemcode,
                serial=tempSerial,
                pta_site=site,
                is_valid=False
            )

            prItem.save()
            tempSerial += 1
    except Exception:
        return tempSerial

    return tempSerial


def buildSpecInfo(spItem, value):
    if not spItem:
        return None

    infoDoc = {}
    infoDoc['id'] = spItem.specification_id
    infoDoc['leaf'] = spItem.leaf_name
    infoDoc['label'] = spItem.label
    infoDoc['type'] = spItem.data_type
    infoDoc['defVal'] = spItem.default_value
    infoDoc['value'] = value

    # Enumerations
    enumList = []
    values = CtgValue.objects.filter(
        specification=spItem).order_by('creation_time')
    for val in values:
        enumDoc = {}
        enumDoc['code'] = val.code
        enumDoc['ctl'] = val.translation
        enumList.append(enumDoc)

    infoDoc['values'] = enumList

    return infoDoc


def populateServiceDoc(service):
    if not service or service.parent_id:
        return None

    biList = [service]
    for fet in PtaBasketItem.objects.filter(parent_id=service.basket_item_id).order_by('itemcode'):
        biList.append(fet)

    biDocList = []
    for item in biList:
        itemDoc = {}
        itemDoc['id'] = item.basket_item_id
        itemDoc['itemcode'] = item.itemcode
        itemDoc['serial'] = item.serial
        itemDoc['leaves'] = []

        for spec in PtaItemLeaf.objects.filter(basket_item=item).order_by('leaf_name'):
            leafDoc = {}
            leafDoc['key'] = spec.leaf_name
            leafDoc['value'] = spec.leaf_value
            itemDoc['leaves'].append(leafDoc)

        biDocList.append(itemDoc)

    return biDocList


def getLeafValueFromSvcDoc(svcDocList, itemcode, leafName):
    if not svcDocList or not itemcode or not leafName:
        return None

    for item in svcDocList:
        if item['itemcode'] == itemcode:
            for leaf in item['leaves']:
                if leaf['key'] == leafName:
                    return leaf['value']
        else:
            continue

    return None


def createOrGetFeature(ctg_doc_id, parentItem):
    if not ctg_doc_id or not parentItem:
        return None
    try:
        # Verify catalog
        parentCtg = CtgProduct.objects.get(
            ctg_doc_id=parentItem.ctg_doc_id, active=True)
        featureCtg = CtgFeature.objects.get(
            ctg_doc_id=ctg_doc_id, product=parentCtg, active=True)

        existFeature = PtaBasketItem.objects.filter(
            parent_id=parentItem.basket_item_id, ctg_doc_id=featureCtg.ctg_doc_id)
        if existFeature and len(existFeature) > 0:
            return existFeature[0]

        newFeature = PtaBasketItem(
            parent_id=parentItem.basket_item_id,
            basket=parentItem.basket,
            ctg_doc_id=featureCtg.ctg_doc_id,
            itemcode=featureCtg.itemcode,
            pta_site=parentItem.pta_site
        )

        newFeature.save()
        return newFeature
    except Exception:
        return None


@transaction.atomic
def createOrUpdateSpec(specId, parentItem, value):
    if not specId or not parentItem:
        return None

    try:
        # Verify catalog
        specCtg = CtgSpecification.objects.get(
            specification_id=specId, parent_ctg_id=parentItem.ctg_doc_id, active=True)

        existSpec = PtaItemLeaf.objects.filter(
            basket_item=parentItem, leaf_name=specCtg.leaf_name)
        if existSpec and len(existSpec) > 0:
            existSpec = existSpec[0]
            existSpec.leaf_value = value
            existSpec.save()
            return existSpec

        newSpec = PtaItemLeaf(
            basket_item=parentItem,
            basket=parentItem.basket,
            leaf_name=specCtg.leaf_name,
            leaf_value=value
        )

        newSpec.save()
        return newSpec
    except Exception:
        return None


@transaction.atomic
def saveBaseSpec(parentItem):
    bsp = 'SP_BASE'

    baseSpec = CtgSpecification.objects.filter(
        parent_ctg_id=parentItem.ctg_doc_id, leaf_name=bsp)
    if baseSpec and len(baseSpec) > 0:
        baseSpec = baseSpec[0]
    else:
        return None

    existSpec = PtaItemLeaf.objects.filter(
        basket_item=parentItem, leaf_name=bsp)
    if existSpec and len(existSpec) > 0:
        return existSpec[0]

    newBaseSpec = PtaItemLeaf(
        basket_item=parentItem,
        basket=parentItem.basket,
        leaf_name=bsp,
        leaf_value='1'
    )

    newBaseSpec.save()
    return newBaseSpec


def getExistingFeature(parentItem, fet_ctg_id):
    try:
        if not parentItem or not fet_ctg_id:
            return None

        return PtaBasketItem.objects.get(parent_id=parentItem.basket_item_id, ctg_doc_id=fet_ctg_id)
    except Exception:
        return None


@transaction.atomic
def validateProductItem(productItem, errorList):
    if not productItem or errorList == None:
        return

    valid = True

    specList = PtaItemLeaf.objects.filter(basket_item=productItem)
    fetList = PtaBasketItem.objects.filter(
        parent_id=productItem.basket_item_id)

    for spec in specList:
        if not validateSpec(spec, productItem.ctg_doc_id, errorList):
            valid = False

    for fet in fetList:
        if not validateFeatureItem(fet, errorList):
            valid = False

    if valid and not productItem.is_valid:
        productItem.is_valid = True
        productItem.save()
    elif productItem.is_valid:
        productItem.is_valid = False
        productItem.save()

    return valid


@transaction.atomic
def validateFeatureItem(featureItem, errorList):
    if not featureItem or errorList == None:
        return

    valid = True

    specList = PtaItemLeaf.objects.filter(basket_item=featureItem)
    for spec in specList:
        if not validateSpec(spec, featureItem.ctg_doc_id, errorList):
            valid = False

    if valid and not featureItem.is_valid:
        featureItem.is_valid = True
        featureItem.save()
    elif not valid and featureItem.is_valid:
        featureItem.is_valid = False
        featureItem.save()

    return valid


def validateSpec(leafItem, parentCtgId, errorList):
    if not leafItem or not parentCtgId or errorList == None:
        return

    try:
        leafVal = leafItem.leaf_value
        specCtg = CtgSpecification.objects.get(
            parent_ctg_id=parentCtgId, leaf_name=leafItem.leaf_name, active=1)
        if specCtg.data_type in ['BO', 'ENUM']:
            return True

        resList = CtgRestriction.objects.filter(specification=specCtg)

        if resList and len(resList) > 0:
            # Check required restriction
            for res in resList:
                if res.rule_type == 'NN' and not leafVal:
                    errorList.append(specCtg.label + ' is required.')
                    return False

            # Check other restrictions
            for res in resList:
                resType = res.rule_type
                resVal = res.value

                if specCtg.data_type == 'STR':
                    if resType == 'UPLEN' and not hasMaxLength(leafVal, int(resVal)):
                        errorList.append(
                            specCtg.label + ' has exceeded ' + resVal + ' character(s).')
                        return False
                    elif resType == 'LOLEN' and not hasMinLength(leafVal, int(resVal)):
                        errorList.append(
                            specCtg.label + ' needs to have at least ' + resVal + ' character(s).')
                        return False
                    elif resType == 'AO' and not hasOnlyLetter(leafVal):
                        errorList.append(
                            specCtg.label + ' can only contain letters.')
                        return False
                    elif resType == 'NUO' and not hasOnlyNumber(leafVal):
                        errorList.append(
                            specCtg.label + ' can only contain digits.')
                        return False
                    elif resType == 'EML' and not isValidEmail(leafVal):
                        errorList.append(
                            specCtg.label + ' is not in valid email format.')
                        return False

                if specCtg.data_type == 'QTY':
                    if not isValidQuantity(leafVal):
                        errorList.append(
                            specCtg.label + ' does not have a valid quantity.')
                        return False
                    elif resType == 'MAX' and not hasMaxValue(leafVal, int(resVal)):
                        errorList.append(
                            specCtg.label + ' should not be greater than ' + resVal + '.')
                        return False
                    elif resType == 'MIN' and not hasMinValue(leafVal, int(resVal)):
                        errorList.append(
                            specCtg.label + ' should not be less than ' + resVal + '.')
                        return False
        else:
            return True

        return True
    except Exception:
        return False
