# Generated by Django 4.0.3 on 2022-07-09 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ColorGameApp', '0017_remove_results_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotteryimages',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
