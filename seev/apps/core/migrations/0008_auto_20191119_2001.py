# Generated by Django 2.2.4 on 2019-11-20 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20191119_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unosite',
            name='zipcode',
            field=models.CharField(max_length=64, verbose_name='Zipcode'),
        ),
    ]
