# Generated by Django 3.1 on 2020-08-20 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0016_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
