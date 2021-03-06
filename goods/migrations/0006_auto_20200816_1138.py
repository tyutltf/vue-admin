# Generated by Django 3.0.8 on 2020-08-16 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_goodsinfotag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfo',
            name='sel',
            field=models.SmallIntegerField(verbose_name='类别'),
        ),
        migrations.AlterField(
            model_name='goodsinfotag',
            name='goodsInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='goods.GoodSInfo', verbose_name='分类标签'),
        ),
    ]
