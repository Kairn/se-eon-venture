import uuid

from django.db import models


class UnoClient(models.Model):
    client_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    le_id = models.UUIDField(default=uuid.uuid4, editable=False)
    ctg_name = models.CharField(max_length=32, unique=True, editable=False)
    entity_name = models.CharField(max_length=255)
    # Add country
    trade_ticker = models.CharField(max_length=12, null=True, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.SlugField(
        max_length=10, help_text='Must be a valid number in the U.S.')
    signature_field = models.BinaryField()
    active = models.BooleanField(default=False, editable=False)
    summary = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'UNO_CLIENT'
