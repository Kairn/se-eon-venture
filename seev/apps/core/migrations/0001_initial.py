# Generated by Django 2.2.3 on 2019-07-14 21:03

from django.db import migrations, models
import seev.apps.utils.country
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnoClient',
            fields=[
                ('client_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('le_id', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Legal Entity ID')),
                ('ctg_name', models.CharField(editable=False, max_length=32, unique=True, verbose_name='Catalog Name')),
                ('entity_name', models.CharField(max_length=255, verbose_name='Entity/Company Name')),
                ('country', models.CharField(choices=[('US', 'United States of America')], default=seev.apps.utils.country.UnoCountry.get_default_cty, max_length=64, verbose_name='Country')),
                ('trade_ticker', models.CharField(blank=True, max_length=12, null=True, verbose_name='Stock Ticker Symbol')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='Contact Email')),
                ('contact_phone', models.SlugField(help_text='Must be a valid number in the U.S.', max_length=10, verbose_name='Contact Phone')),
                ('signature_letter', models.BinaryField(verbose_name='Signature Letter of Agreement')),
                ('active', models.BooleanField(default=False, editable=False)),
                ('summary', models.TextField(blank=True, null=True, verbose_name='Business Summary')),
                ('website', models.CharField(blank=True, max_length=255, null=True, verbose_name='Business Website')),
            ],
            options={
                'db_table': 'UNO_CLIENT',
            },
        ),
    ]