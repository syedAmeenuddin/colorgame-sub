# Generated by Django 3.0.3 on 2022-07-01 19:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ColorGameApp', '0007_auto_20220701_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamedetails',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]
