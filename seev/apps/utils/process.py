"""
Handle background tasks used by view logic
"""

from django.db import transaction

from seev.apps.core.models import *
from seev.apps.catalog.models import *
from seev.apps.order.models import *

from seev.apps.utils.generators import *
from seev.apps.utils.session import *


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
