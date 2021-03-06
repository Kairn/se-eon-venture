# Generated by Django 3.0 on 2019-12-28 00:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20191217_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='ptasite',
            name='is_priced',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ptaorderinstance',
            name='status',
            field=models.CharField(choices=[('IN', 'Initiated'), ('IP', 'In Progress'), ('VA', 'Validated'), ('FL', 'Finalized'), ('FZ', 'Frozen'), ('EX', 'Expired'), ('VD', 'Voided')], max_length=16, verbose_name='Status'),
        ),
        migrations.CreateModel(
            name='PtaPriceLine',
            fields=[
                ('price_line_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('charge_type', models.CharField(choices=[('QUAN', 'Quantity Based'), ('SPEC', 'Specification Based'), ('ONTM', 'One-Time Charge')], max_length=16, verbose_name='Charge Type')),
                ('mrc_charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('nrc_charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Timestamp of Creation')),
                ('basket_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.PtaBasketItem')),
                ('item_leaf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.PtaItemLeaf')),
            ],
        ),
    ]
