# Generated by Django 3.0.8 on 2020-08-14 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20200813_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodSInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='分类参数名称')),
                ('sel', models.SmallIntegerField(max_length=1, verbose_name='类别')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='goods.GoodsLevelThree', verbose_name='所属分类')),
            ],
            options={
                'verbose_name': '商品参数',
                'verbose_name_plural': '商品参数',
                'ordering': ['-create_date'],
            },
        ),
    ]