# Generated by Django 2.2.4 on 2019-09-17 00:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctgfeature',
            name='limit',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='ctgspecification',
            name='default_value',
            field=models.CharField(default='N/A', max_length=512, verbose_name='Default Value'),
        ),
        migrations.AlterField(
            model_name='ctgspecification',
            name='data_type',
            field=models.CharField(choices=[('BO', 'Boolean'), ('STR', 'String'), ('QTY', 'Quantity'), ('ENUM', 'Enumeration')], max_length=32, verbose_name='Data Type'),
        ),
        migrations.AlterField(
            model_name='ctgspecification',
            name='leaf_name',
            field=models.CharField(max_length=32, verbose_name='Specification Code'),
        ),
        migrations.CreateModel(
            name='CtgValue',
            fields=[
                ('value_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=16)),
                ('translation', models.CharField(max_length=128)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Timestamp of Creation')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.CtgSpecification')),
            ],
            options={
                'db_table': 'CTG_VALUE',
            },
        ),
        migrations.CreateModel(
            name='CtgRestriction',
            fields=[
                ('restriction_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rule_type', models.CharField(choices=[('MAX', 'Maximum Value'), ('MIN', 'Minimum Value'), ('UPLEN', 'Length Upper Limit'), ('LOLEN', 'Length Lower Limit'), ('AO', 'Alphabetical Letters Only'), ('NUO', 'Numbers Only'), ('EML', 'Email Format'), ('CD', 'Must Be Divisible By')], max_length=32, verbose_name='Rule Type')),
                ('value', models.CharField(default='1', max_length=64, null=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Timestamp of Creation')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.CtgSpecification')),
            ],
            options={
                'db_table': 'CTG_RESTRICTION',
            },
        ),
        migrations.CreateModel(
            name='CtgPrice',
            fields=[
                ('price_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ctg_doc_id', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Catalog Obect ID')),
                ('mrc', models.DecimalField(decimal_places=2, default=1.0, max_digits=16, null=True)),
                ('nrc', models.DecimalField(decimal_places=2, default=1.0, max_digits=16, null=True)),
                ('unit_mrc', models.DecimalField(decimal_places=2, default=0.0, max_digits=16, null=True)),
                ('unit_nrc', models.DecimalField(decimal_places=2, default=0.0, max_digits=16, null=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Timestamp of Creation')),
                ('value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.CtgValue')),
            ],
            options={
                'db_table': 'CTG_PRICE',
            },
        ),
    ]
