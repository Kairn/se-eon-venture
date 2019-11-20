"""
Model definitions in core app
"""

import uuid

from django.db import models
from django.utils.timezone import now

from seev.apps.utils.country import UnoCountry
from seev.apps.utils.state import UnoState


class UnoClient(models.Model):
    client_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    le_id = models.UUIDField(
        'Legal Entity ID', default=uuid.uuid4, editable=False)
    ctg_name = models.CharField(
        'Catalog Name', max_length=32, unique=True, editable=False)
    entity_name = models.CharField('Entity/Company Name', max_length=255)
    country = models.CharField(
        'Country', max_length=64, default=UnoCountry.get_default_cty, choices=UnoCountry.get_cty_code_list())
    trade_ticker = models.CharField(
        'Stock Ticker Symbol', max_length=12, null=True, blank=True)
    contact_email = models.EmailField('Contact Email')
    contact_phone = models.SlugField(
        'Contact Phone', max_length=10, help_text='Must be a valid number in the U.S.')
    signature_letter = models.BinaryField('Signature Letter of Agreement')
    active = models.BooleanField(default=False, editable=False)
    status = models.CharField('Status', max_length=16,
                              default='Pending', editable=False, null=False)
    summary = models.TextField('Business Summary', null=True, blank=True)
    website = models.CharField(
        'Business Website', max_length=255, null=True, blank=True)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'UNO_CLIENT'


class UnoCredentials(models.Model):
    credentials_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    username = models.CharField(
        'Username', max_length=32, null=False, unique=True)
    password_salt = models.CharField(max_length=8, editable=False)
    password_hash = models.CharField(
        max_length=1024, editable=False, null=False)
    recovery_email = models.EmailField(
        'Recovery Email', help_text='Email used to reset password', unique=True)
    pin = models.PositiveSmallIntegerField(
        'PIN', help_text='PIN is required to reset password')
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'UNO_CREDENTIALS'


class UnoApproval(models.Model):
    approval_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        UnoClient, on_delete=models.CASCADE, null=False, blank=False)
    action = models.CharField('Action', max_length=16, choices=[
        ('AP', 'Approve Request'),
        ('DE', 'Deny Request'),
        ('RV', 'Revoke Business'),
        ('RI', 'Reinstate Business'),
    ], null=False, blank=False)
    message = models.TextField('Message/Comment', null=True, blank=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'UNO_APPROVAL'


class UnoCustomer(models.Model):
    customer_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    le_id = models.UUIDField('Customer Entity ID',
                             default=uuid.uuid4, editable=False)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    customer_name = models.CharField('Customer Name', max_length=255)
    contact_email = models.EmailField('Contact Email')
    country = models.CharField(
        'Country', max_length=64, default=UnoCountry.get_default_cty, choices=UnoCountry.get_cty_code_list())
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'UNO_CUSTOMER'


class UnoOpportunity(models.Model):
    opportunity_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    opportunity_number = models.UUIDField(
        'Opportunity Number', default=uuid.uuid4, editable=False)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(
        UnoCustomer, on_delete=models.CASCADE, null=False)
    active = models.BooleanField(default=True, editable=False)
    discount_nrc = models.CharField('Non-recurring Discount', max_length=16, choices=[
        ('0', 'No Discount'),
        ('5', '5% Discount'),
        ('10', '10% Discount'),
        ('15', '15% Discount'),
        ('20', '20% Discount'),
        ('25', '25% Discount'),
        ('30', '30% Discount'),
    ], null=False, blank=False)
    discount_mrc = models.CharField('Monthly Discount', max_length=16, choices=[
        ('0', 'No Discount'),
        ('5', '5% Discount'),
        ('10', '10% Discount'),
        ('15', '15% Discount'),
        ('20', '20% Discount'),
        ('25', '25% Discount'),
        ('30', '30% Discount'),
    ], null=False, blank=False)
    deal_count = models.PositiveSmallIntegerField(
        'Deal Count', editable=False, default=0)
    deal_limit = models.PositiveSmallIntegerField('Deal Limit', default=1)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'UNO_OPPORTUNITY'


class UnoOrder(models.Model):
    order_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.UUIDField('Order Number', editable=False)
    client = models.ForeignKey(UnoClient, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(
        UnoCustomer, on_delete=models.CASCADE, null=False)
    opportunity = models.ForeignKey(
        UnoOpportunity, on_delete=models.CASCADE, null=False)
    status = models.CharField('status', max_length=16, choices=[
        ('CL', 'Cancelled'),
        ('SM', 'Submitted'),
        ('RN', 'Renegotiated'),
        ('IV', 'Invalidated'),
        ('OD', 'Ordered'),
        ('CP', 'Completed'),
    ], null=False, blank=False)
    order_data_1 = models.TextField('Data Chunk 1', max_length=4000, null=True)
    order_data_2 = models.TextField('Data Chunk 2', max_length=4000, null=True)
    order_data_3 = models.TextField('Data Chunk 3', max_length=4000, null=True)
    data_length = models.PositiveIntegerField('Data Length in Characters')
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)
    last_update_time = models.DateTimeField(
        'Timestamp of Last Update', default=now, editable=False, null=False)

    class Meta:
        db_table = 'UNO_ORDER'


class UnoSite(models.Model):
    site_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    location_id = models.UUIDField(
        'Location ID', default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        UnoCustomer, on_delete=models.CASCADE, null=False)
    address_1 = models.CharField(
        'Address Line 1', max_length=512, null=False, blank=False)
    address_2 = models.CharField('Address Line 2', max_length=128, null=True)
    address_3 = models.CharField('Address Line 3', max_length=128, null=True)
    city = models.CharField('City', max_length=64)
    state = models.CharField('State or Province', max_length=64)
    zipcode = models.CharField('Zipcode', max_length=64)
    country = models.CharField('Country', max_length=256, null=False)
    is_virtual = models.BooleanField(default=False)
    creation_time = models.DateTimeField(
        'Timestamp of Creation', default=now, editable=False, null=False)

    class Meta:
        db_table = 'UNO_SITE'
