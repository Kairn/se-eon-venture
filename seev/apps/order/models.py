"""
Model definitions in order app
"""

import uuid

from django.db import models
from django.utils.timezone import now

from seev.apps.core.models import (
    UnoClient, UnoSite, UnoCustomer, UnoOpportunity)


class PtaBasket(models.Model):
    basket_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(
        UnoCustomer, on_delete=models.CASCADE, null=False)
    is_locked = models.BooleanField(default=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'PTA_BASKET'


class PtaOrderInstance(models.Model):
    order_instance_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.UUIDField(
        'Order Number', default=uuid.uuid4, editable=False)
    order_name = models.CharField(
        'Order Name', max_length=32, default=None, null=True)
    secret = models.CharField('Order Secret', max_length=64, default=None)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(
        UnoCustomer, on_delete=models.CASCADE, null=False)
    opportunity = models.ForeignKey(
        UnoOpportunity, on_delete=models.CASCADE, null=False)
    basket = models.ForeignKey(
        PtaBasket, on_delete=models.SET_NULL, null=True)
    status = models.CharField('Status', max_length=16, choices=[
        ('IN', 'Initiated'),
        ('IP', 'In Progress'),
        ('VA', 'Validated'),
        ('FL', 'Finalized'),
        ('FZ', 'Frozen'),
        ('EX', 'Expired'),
        ('VD', 'Voided'),
    ], null=False, blank=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'PTA_ORDER_INSTANCE'


class PtaSite(models.Model):
    pta_site_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    site_name = models.CharField('Site Name', max_length=128, null=True)
    site = models.ForeignKey(UnoSite, on_delete=models.SET_NULL, null=True)
    order_instance = models.ForeignKey(
        PtaOrderInstance, on_delete=models.CASCADE, null=False)
    is_valid = models.BooleanField(default=False)
    is_priced = models.BooleanField(default=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'PTA_SITE'


class PtaBasketItem(models.Model):
    basket_item_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    parent_id = models.UUIDField('Parent Item ID', editable=False, null=True)
    basket = models.ForeignKey(PtaBasket, on_delete=models.CASCADE, null=False)
    ctg_doc_id = models.UUIDField(
        'Catalog Item ID', editable=False, null=False)
    itemcode = models.CharField('Item Code', max_length=32, null=False)
    serial = models.PositiveSmallIntegerField(
        'Serial Number', default=0, null=True)
    pta_site = models.ForeignKey(PtaSite, on_delete=models.CASCADE, null=False)
    is_valid = models.BooleanField(default=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'PTA_BASKET_ITEM'


class PtaItemLeaf(models.Model):
    leaf_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    basket_item = models.ForeignKey(
        PtaBasketItem, on_delete=models.CASCADE, null=False)
    basket = models.ForeignKey(PtaBasket, on_delete=models.CASCADE, null=False)
    leaf_name = models.CharField(
        'Leaf Name', max_length=32, null=False, unique=False)
    leaf_value = models.CharField('Leaf Value', max_length=512, default=None)

    class Meta:
        db_table = 'PTA_ITEM_LEAF'


class PtaPriceLine(models.Model):
    price_line_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    basket_item = models.ForeignKey(
        PtaBasketItem, on_delete=models.CASCADE, null=False)
    item_leaf = models.ForeignKey(
        PtaItemLeaf, on_delete=models.CASCADE, null=False)
    charge_type = models.CharField('Charge Type', max_length=16, choices=[
        ('QUAN', 'Quantity Based'),
        ('SPEC', 'Specification Based'),
        ('ONTM', 'One-Time Charge'),
    ], null=False, blank=False)
    mrc_charge = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.00, null=True)
    nrc_charge = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.00, null=True)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)
