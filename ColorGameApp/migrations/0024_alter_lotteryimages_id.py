# Generated by Django 4.0.3 on 2022-07-12 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ColorGameApp', '0023_auto_20220710_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotteryimages',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]