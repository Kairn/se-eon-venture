"""
Model definitions in catalog app
"""

import uuid

from django.db import models
from django.utils.timezone import now

from seev.apps.core.models import UnoClient


class CtgProduct(models.Model):
    product_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ctg_doc_id = models.UUIDField(
        'Catalog Obect ID', default=uuid.uuid4, editable=False)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    itemcode = models.CharField(
        'Product Code', max_length=32, null=False, unique=True)
    name = models.CharField('Product Name', max_length=128, null=False)
    active = models.BooleanField(default=True, editable=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'CTG_PRODUCT'
