# Generated by Django 3.0.3 on 2022-07-05 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ColorGameApp', '0014_gamedetails_resultid'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='result',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
