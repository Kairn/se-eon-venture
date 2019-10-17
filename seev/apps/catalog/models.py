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


class CtgFeature(models.Model):
    feature_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ctg_doc_id = models.UUIDField(
        'Catalog Obect ID', default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        CtgProduct, on_delete=models.CASCADE, null=False)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    itemcode = models.CharField(
        'Feature Code', max_length=32, null=False, unique=True)
    name = models.CharField('Feature Name', max_length=128, null=False)
    limit = models.PositiveSmallIntegerField(default=1)
    extended = models.CharField('Extended Only', max_length=8, null=True)
    active = models.BooleanField(default=True, editable=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'CTG_FEATURE'


class CtgSpecification(models.Model):
    specification_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ctg_doc_id = models.UUIDField(
        'Catalog Obect ID', default=uuid.uuid4, editable=False)
    parent_ctg_id = models.UUIDField(
        'Parent Item ID', editable=False, null=False)
    leaf_name = models.CharField(
        'Specification Code', max_length=32, null=False, unique=False)
    label = models.CharField('Specification Name', max_length=128, null=False)
    data_type = models.CharField('Data Type', max_length=32, choices=[
        ('BO', 'Boolean'),
        ('STR', 'String'),
        ('QTY', 'Quantity'),
        ('ENUM', 'Enumeration'),
    ], null=False, blank=False)
    default_value = models.CharField(
        'Default Value', max_length=512, default='N/A')
    active = models.BooleanField(default=True, editable=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'CTG_SPECIFICATION'


class CtgValue(models.Model):
    value_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    specification = models.ForeignKey(
        CtgSpecification, on_delete=models.CASCADE, null=False)
    code = models.CharField(max_length=16, null=False, blank=False)
    translation = models.CharField(max_length=128, null=False, blank=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'CTG_VALUE'


class CtgRestriction(models.Model):
    restriction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    specification = models.ForeignKey(
        CtgSpecification, on_delete=models.CASCADE, null=False)
    rule_type = models.CharField('Rule Type', max_length=32, choices=[
        ('MAX', 'Maximum Value'),
        ('MIN', 'Minimum Value'),
        ('UPLEN', 'Length Upper Limit'),
        ('LOLEN', 'Length Lower Limit'),
        ('AO', 'Alphabetical Letters Only'),
        ('NUO', 'Numbers Only'),
        ('EML', 'Email Format'),
        ('NN', 'Not Null')
    ], null=False, blank=False)
    value = models.CharField(max_length=64, null=True, default='1')
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'CTG_RESTRICTION'


class CtgPrice(models.Model):
    price_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ctg_doc_id = models.UUIDField(
        'Catalog Obect ID', default=uuid.uuid4, editable=False)
    mrc = models.DecimalField(
        max_digits=16, decimal_places=2, default=1.00, null=True)
    nrc = models.DecimalField(
        max_digits=16, decimal_places=2, default=1.00, null=True)
    unit_mrc = models.DecimalField(
        max_digits=16, decimal_places=2, default=0.00, null=True)
    unit_nrc = models.DecimalField(
        max_digits=16, decimal_places=2, default=0.00, null=True)
    value = models.ForeignKey(CtgValue, on_delete=models.CASCADE, null=True)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'CTG_PRICE'
