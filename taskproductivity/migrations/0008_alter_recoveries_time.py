# Generated by Django 3.2.3 on 2021-10-06 01:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taskproductivity', '0007_auto_20210923_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recoveries',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]