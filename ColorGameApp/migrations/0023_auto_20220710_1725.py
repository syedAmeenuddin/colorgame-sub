# Generated by Django 3.0.3 on 2022-07-10 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ColorGameApp', '0022_alter_bankdetails_user_alter_upidetails_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lotteryimages',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
