# Generated by Django 3.0.8 on 2020-07-25 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0003_auto_20200724_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='dpname',
        ),
        migrations.AlterField(
            model_name='orderq',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('EXECUTED', 'Executed'), ('FAILED', 'Failed'), ('COMPLETE', 'Complete'), ('CANCELLED', 'Cancelled')], default='EXECUTED', max_length=10),
        ),
    ]
