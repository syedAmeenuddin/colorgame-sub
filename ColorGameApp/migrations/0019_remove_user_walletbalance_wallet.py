# Generated by Django 4.0.3 on 2022-07-09 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ColorGameApp', '0018_alter_lotteryimages_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='walletBalance',
        ),
        migrations.CreateModel(
            name='wallet',
            fields=[
                ('walletId', models.AutoField(primary_key=True, serialize=False)),
                ('walletBalance', models.CharField(blank=True, default=0, max_length=7, null=True)),
                ('user', models.ForeignKey(blank=True, max_length=10, null=True, on_delete=django.db.models.deletion.CASCADE, to='ColorGameApp.user')),
            ],
        ),
    ]
