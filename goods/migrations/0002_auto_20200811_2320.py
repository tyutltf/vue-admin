# Generated by Django 3.0.8 on 2020-08-11 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodslevelthree',
            old_name='previous',
            new_name='GoodsLevelTwo',
        ),
        migrations.RenameField(
            model_name='goodsleveltwo',
            old_name='previous',
            new_name='GoodsLevelOne',
        ),
    ]