# Generated by Django 3.2.3 on 2021-09-23 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskproductivity', '0006_auto_20210923_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erdates',
            name='entry',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='erdates',
            name='renewal',
            field=models.DateField(null=True),
        ),
    ]
