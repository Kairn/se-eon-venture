# Generated by Django 2.2.4 on 2019-09-14 00:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0005_unoopportunity'),
    ]

    operations = [
        migrations.CreateModel(
            name='CtgSpecification',
            fields=[
                ('specification_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ctg_doc_id', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Catalog Obect ID')),
                ('parent_ctg_id', models.UUIDField(editable=False, verbose_name='Parent Item ID')),
                ('leaf_name', models.CharField(max_length=32, unique=True, verbose_name='Specification Code')),
                ('label', models.CharField(max_length=128, verbose_name='Specification Name')),
                ('data_type', models.CharField(choices=[('BO', 'Boolean'), ('STR', 'String'), ('NUM', 'Number'), ('ENUM', 'Enumeration'), ('SLG', 'Slug'), ('AT', 'Auto')], max_length=32, verbose_name='Data Type')),
                ('active', models.BooleanField(default=True, editable=False)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Timestamp of Creation')),
            ],
            options={
                'db_table': 'CTG_SPECIFICATION',
            },
        ),
        migrations.CreateModel(
            name='CtgProduct',
            fields=[
                ('product_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ctg_doc_id', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Catalog Obect ID')),
                ('itemcode', models.CharField(max_length=32, unique=True, verbose_name='Product Code')),
                ('name', models.CharField(max_length=128, verbose_name='Product Name')),
                ('active', models.BooleanField(default=True, editable=False)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Timestamp of Creation')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UnoClient')),
            ],
            options={
                'db_table': 'CTG_PRODUCT',
            },
        ),
        migrations.CreateModel(
            name='CtgFeature',
            fields=[
                ('feature_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ctg_doc_id', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Catalog Obect ID')),
                ('itemcode', models.CharField(max_length=32, unique=True, verbose_name='Feature Code')),
                ('name', models.CharField(max_length=128, verbose_name='Feature Name')),
                ('active', models.BooleanField(default=True, editable=False)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Timestamp of Creation')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UnoClient')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.CtgProduct')),
            ],
            options={
                'db_table': 'CTG_FEATURE',
            },
        ),
    ]