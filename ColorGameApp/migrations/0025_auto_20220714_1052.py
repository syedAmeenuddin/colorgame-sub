# Generated by Django 3.0.3 on 2022-07-14 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ColorGameApp', '0024_alter_lotteryimages_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotteryimages',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
