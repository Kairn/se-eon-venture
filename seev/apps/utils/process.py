"""
Handle background tasks used by view logic
"""

from django.db import transaction

from seev.apps.core.models import *
from seev.apps.catalog.models import *
from seev.apps.order.models import *


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


def getAllSitesInOrder(order):
    if not order:
        return None

    return PtaSite.objects.filter(order_instance=order)


def getAllProductsInOrder(order):
    if not order:
        return None

    return PtaBasketItem.objects.filter(basket=order.basket, parent_id=None)
