# Generated by Django 4.0.3 on 2022-07-09 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ColorGameApp', '0020_alter_bankdetails_accountnumber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdetails',
            name='accountNumber',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bankdetails',
            name='ifsc',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bankdetails',
            name='recipientName',
            field=models.CharField(max_length=100),
        ),
    ]
