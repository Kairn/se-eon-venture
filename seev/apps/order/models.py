"""
Model definitions in order app
"""

import uuid

from django.db import models
from django.utils.timezone import now

from seev.apps.core.models import (
    UnoClient, UnoSite, UnoCustomer, UnoOpportunity)


class PtaOrderInstance(models.Model):
    order_instance_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.UUIDField(
        'Order Number', default=uuid.uuid4, editable=False)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(
        UnoCustomer, on_delete=models.CASCADE, null=False)
    opportunity = models.ForeignKey(
        UnoOpportunity, on_delete=models.CASCADE, null=False)
    basket = models.ForeignKey(
        PtaBasket, on_delete=models.SET_NULL, null=False)
    status = models.CharField('status', max_length=16, choices=[
        ('IN', 'Initiated'),
        ('IP', 'In Progress'),
        ('CL', 'Cancelled'),
        ('VA', 'Validated'),
        ('PD', 'Priced'),
        ('FL', 'Finalized'),
        ('FZ', 'Frozen'),
        ('EX', 'Expired'),
        ('VD', 'Voided'),
    ], null=False, blank=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'PTA_ORDER_INSTANCE'


class PtaBasket(models.Model):
    basket_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(
        UnoCustomer, on_delete=models.CASCADE, null=False)
    order_number = models.UUIDField('Order Number', editable=False)
    is_locked = models.BooleanField(default=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'PTA_BASKET'


class PtaSite(models.Model):
    pta_site_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    site = models.ForeignKey(UnoSite, on_delete=models.SET_NULL, null=False)
    order_instance = models.ForeignKey(
        PtaOrderInstance, on_delete=models.CASCADE, null=False)
    is_valid = models.BooleanField(default=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'PTA_SITE'
