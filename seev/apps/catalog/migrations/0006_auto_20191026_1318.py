# Generated by Django 2.2.4 on 2019-10-26 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20191019_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctgspecification',
            name='default_value',
            field=models.CharField(default=None, max_length=512, verbose_name='Default Value'),
        ),
    ]
