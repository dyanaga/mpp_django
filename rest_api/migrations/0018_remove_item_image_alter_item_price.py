# Generated by Django 4.1.7 on 2023-03-29 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_rest_api', '0017_orderitem_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(),
        ),
    ]
