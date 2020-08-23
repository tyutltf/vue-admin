# Generated by Django 3.1 on 2020-08-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0013_auto_20200818_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsproductlist',
            name='goods_content',
            field=models.TextField(blank=True, null=True, verbose_name='商品内容'),
        ),
        migrations.AddField(
            model_name='goodsproductlist',
            name='goods_image',
            field=models.ManyToManyField(blank=True, null=True, to='goods.GoodsImage', verbose_name='商品图片'),
        ),
    ]
