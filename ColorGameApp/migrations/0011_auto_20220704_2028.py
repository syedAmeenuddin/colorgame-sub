# Generated by Django 3.0.3 on 2022-07-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ColorGameApp', '0010_auto_20220702_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamedetails',
            name='date',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='gamedetails',
            name='time',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
