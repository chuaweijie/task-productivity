# Generated by Django 3.1.2 on 2021-06-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskproductivity', '0004_auto_20210624_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]