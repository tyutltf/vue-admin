# Generated by Django 3.0.8 on 2020-08-16 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remove_role_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]